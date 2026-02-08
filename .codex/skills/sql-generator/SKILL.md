---
name: sql-generator
description: リポジトリ内のスキーマドキュメントを根拠にSQLを生成する
---

# SQL Generator

- `docs/` 配下のYAMLファイルにはDBのスキーマ定義が記載されているので、まずは読むこと
- 上記ファイルを根拠にSQLを生成すること
- 要件が曖昧な場合は、SQLを確定する前に不足条件を質問する

## ファイルの形式
- ファイルに記載された `name` をテーブル名、`fields[].name` をカラム名として扱う
- `fields[].verbose_name` は人間向けの表示名として扱い、SQL上の識別子には `fields[].name` を使う
- `fields[].choices` は列挙値定義（`value` / `label`）として扱い、SQL上の比較・更新には原則 `value` を使う
- `doc.title` はテーブルの業務上の名称、`doc.description` は説明、`doc.context` は利用上の前提・ルールとして扱う
- `constraints` には制約が記載される

## SQL作成ルール
1. ユーザー要求から対象テーブルと必要カラムを特定する
2. `docs/*.yml` を参照し、存在しないテーブル/カラム名は使わない
3. JOINは `relation` に基づくキーで行う
4. 一意制約や `is_null` を無視しない
5. `choices` が定義されたカラムは、定義済みの許容値のみを条件・更新値に使う
6. ユーザーが `choices` の `label` で指定した場合は、対応する `value` に読み替えてSQLを作成する

## 出力フォーマット
- SQL本体をコードブロックで提示
- その後に根拠として参照したテーブル/カラムを箇条書きで簡潔に記載
- `choices` を使った場合は、使用した `label` / `value` の対応を根拠に明記
- 必要に応じて前提条件（DB方言、タイムゾーン、NULLの扱い）を明記
