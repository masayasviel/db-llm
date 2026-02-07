from django.db import models

# Create your models here.


class Group(models.Model):
    """
    :title: グループ
    :description: ユーザをまとめるグループ
    :context: 階層構造を取る
    :context: 階層の深さに制限はない
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True, verbose_name="グループ名")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, verbose_name="親グループ")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="group_name_uniq"),
        ]
        db_table = "group"


class User(models.Model):
    """
    :title: ユーザ-
    """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, verbose_name="ユーザー名")
    code = models.CharField(max_length=256, unique=True, verbose_name="ユーザーユニークコード")

    class Meta:
        db_table = "user"


class GroupUserRelation(models.Model):
    """
    :title: ユーザ-とグループの紐付け
    :context: ユーザーは複数グループに所属できる
    """

    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "group_user_relation"


class Tag(models.Model):
    """
    :title: タグ
    :description: 記事やユーザーなどにタグをつけることができる
    :context: 公式タグフラグがtrueなら、サービス提供者が用意したタグであることを示す
    :context: タグはユーザーが任意に作成でき、それを他ユーザーが利用できる
    """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True, verbose_name="タグ名")
    is_official = models.BooleanField(default=False, verbose_name="公式タグフラグ")

    class Meta:
        db_table = "tag"


class UserTagRelation(models.Model):
    """
    :title: ユーザ-とタグの紐付け
    :context: ユーザーのタグフォロー状況
    :context: フォローを外せばレコードが削除される
    """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "tag"], name="user_and_tag_uniq"),
        ]
        indexes = [
            models.Index(fields=["user", "tag"]),
        ]
        db_table = "user_tag_relation"


class Article(models.Model):
    """
    :title: 記事
    """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256, verbose_name="記事タイトル", db_index=True)
    article_path = models.TextField(verbose_name="記事実態の保存先パス", help_text="記事の内容と記事内のメディアはそこに保存される")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="記事の作成者")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="article_title_and_user_uniq"),
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
