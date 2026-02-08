from collections import defaultdict
from pathlib import Path

import yaml
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import BaseConstraint, Field
from docutils import nodes
from docutils.core import publish_doctree


class Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


class Command(BaseCommand):
    help = "model_to_document"
    ALLOW_APP_LABEL = ("defaultdb",)

    def handle(self, *args, **options):
        models_info: dict[str, list[dict]] = defaultdict(list)

        for model in apps.get_models():
            meta = model._meta

            if meta.app_label not in self.ALLOW_APP_LABEL:
                continue

            doc = self._rst_field_list_to_dict(model.__doc__ or "")

            fields = []
            for f in meta.fields:
                preferred_name = self._serialize_choices(field=f)

                fields.append(
                    {
                        k: v
                        for k, v in {
                            "name": f.name,
                            "type": f.get_internal_type(),
                            "choices": preferred_name,
                            "verbose_name": str(f.verbose_name) if f.verbose_name else None,
                            "help_text": f.help_text or None,
                            "is_null": f.null,
                            "is_allow_blank": f.blank,
                            "is_unique": f.unique,
                            "primary_key": f.primary_key,
                            "relation": (f.remote_field.model.__name__ if f.is_relation and f.remote_field else None),
                            "index": f.db_index,
                        }.items()
                        if v is not None
                    }
                )

            models_info[model.__module__].append(
                {
                    "name": meta.db_table,
                    "doc": doc,
                    "fields": fields,
                    "constraints": [self._serialize_constraint(c) for c in meta.constraints],
                    "index": [{"name": idx.name, "fields": list(idx.fields or [])} for idx in meta.indexes],
                }
            )

        out_dir = Path(settings.BASE_DIR).parent / "docs"
        out_dir.mkdir(parents=True, exist_ok=True)

        for k, v in models_info.items():
            module_name = k.split(".")[-1]
            out_path = out_dir / f"{module_name}.yml"
            with out_path.open("w+", encoding="utf-8") as f:
                yaml.dump(v, f, default_flow_style=False, allow_unicode=True, sort_keys=False, Dumper=Dumper)

    def _rst_field_list_to_dict(self, rst: str) -> dict:
        doctree = publish_doctree(rst or "")
        result = {}

        for field in doctree.traverse(nodes.field):
            key = field.children[0].astext().strip()
            val = field.children[1].astext().strip()

            if key in result:
                if isinstance(result[key], list):
                    result[key].append(val)
                else:
                    result[key] = [result[key], val]
            else:
                result[key] = val

        return result

    def _serialize_constraint(self, constraint: BaseConstraint) -> dict:
        data = {
            "type": constraint.__class__.__name__,
            "fields": list(getattr(constraint, "fields", None) or []),
            "name": constraint.name,
        }

        if (condition := getattr(constraint, "condition", None)) is not None:
            data["condition"] = str(condition)

        return data

    def _serialize_choices(
        self,
        field: Field,
    ) -> list | None:

        def _normalize_choices(raw_choices) -> list[dict[str, str]]:
            normalized: list[dict[str, str]] = []
            for choice in raw_choices:
                if not isinstance(choice, (list, tuple)) or len(choice) != 2:
                    continue

                value, label = choice
                if not isinstance(label, str):
                    continue

                normalized.append({"value": str(value), "label": str(label)})

            return normalized

        raw_choices = getattr(field, "choices", None)
        if not raw_choices:
            return None

        serialized_choices = _normalize_choices(raw_choices)
        if not serialized_choices:
            return None

        return serialized_choices
