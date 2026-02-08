from django.db import models

# Create your models here.


class Group(models.Model):
    """
    :title: グループ
    :description: ユーザをまとめるグループ
    :context: 階層構造を取る
    :context: parent=nullであれば、最上位グループとする
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
    code = models.CharField(max_length=256, unique=True, db_index=True, verbose_name="ユーザーユニークコード")

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
        db_table = "user_tag_relation"
