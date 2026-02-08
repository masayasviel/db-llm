from django.db import models

from .master import Tag, User

# Create your models here.


class Article(models.Model):
    """
    :title: 記事
    """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256, verbose_name="記事タイトル")
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
