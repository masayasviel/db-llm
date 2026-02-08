from django.db import models

from .constants import ARTICLE_STATUS, CAMPAIGN_TYPE
from .master import Group, Tag, User

# Create your models here.


class Campaign(models.Model):
    """
    :title: キャンペーン
    :context: 記事に紐づけられるイベント
    :context: キャンペーンは運営のみ作成できる
    """

    id = models.AutoField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    name = models.CharField(max_length=256, verbose_name="イベント名")
    type = models.CharField(
        max_length=16,
        choices=CAMPAIGN_TYPE,
        default="OFFICIAL",
        verbose_name="キャンペーンタイプ",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="対象グループ",
    )
    description = models.CharField(max_length=1000, blank=True, verbose_name="イベント概要")
    start_at = models.DateTimeField(verbose_name="イベント開始日時")
    end_at = models.DateTimeField(verbose_name="イベント終了日時")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_at__gte=models.F("start_at")),
                name="campaign_period_valid",
            ),
            models.CheckConstraint(
                condition=(models.Q(type="OFFICIAL", group__isnull=True) | models.Q(type__in=("CLIENT", "GROUP"), group__isnull=False)),
                name="campaign_type_group_valid",
            ),
        ]
        db_table = "campaign"


class Article(models.Model):
    """
    :title: 記事
    :context: ユーザーごとの記事一覧は公開状態と更新日時で絞り込み・並び替えされる
    :context: 公開中記事は公開状態と公開日時で取得される
    """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256, verbose_name="記事タイトル")
    article_path = models.TextField(verbose_name="記事実態の保存先パス", help_text="記事の内容と記事内のメディアはそこに保存される")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="記事の作成者")
    status = models.CharField(max_length=16, choices=ARTICLE_STATUS, default="DRAFT", verbose_name="公開状態")
    published_at = models.DateTimeField(null=True, verbose_name="公開日時")
    deleted_at = models.DateTimeField(null=True, verbose_name="削除日時")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="article_title_and_user_uniq"),
            models.CheckConstraint(
                condition=models.Q(status="DRAFT", published_at__isnull=True, deleted_at__isnull=True)
                | models.Q(status="PUBLISHED", published_at__isnull=False, deleted_at__isnull=True)
                | models.Q(status="ARCHIVED", published_at__isnull=False, deleted_at__isnull=False),
                name="article_status_datetime_valid",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"], name="article_user_status_updated_idx"),
            models.Index(fields=["status", "published_at"], name="article_status_published_idx"),
        ]
        db_table = "article"


class ArticleTagRelation(models.Model):
    """
    :title: 記事へのタグ付け
    :context: ユーザーが記事にタグ付けできる
    :context: タグを外せばレコードが削除される
    """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="タグの付与者")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["article", "tag"], name="article_and_tag_uniq"),
        ]
        db_table = "article_tag_relation"


class ArticleCampaignRelation(models.Model):
    """
    :title: 記事とキャンペーンの紐付け
    :context: 記事はキャンペーンに0または1つ紐づく
    """

    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["article"], name="article_campaign_article_uniq"),
        ]
        db_table = "article_campaign_relation"
