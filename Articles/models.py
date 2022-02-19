from django.db import models
from GraphQL.models import BaseModel, BaseModelName
from djongo.models import ArrayField
from Persons.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


# Create your models here.


MAX_LENGTH = 100


class Tag(BaseModelName):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Article(BaseModel):
    title = models.CharField(max_length=MAX_LENGTH, blank=False, null=False)
    slug = models.SlugField(
        max_length=MAX_LENGTH,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    # TODO Djongo Array Field
    tags = ArrayField(
        model_container=Tag,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title


class Comment(BaseModel):
    body = models.TextField()
    article = models.ForeignKey(
        Article,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return str(self.article)


class FavoriteArticles(BaseModel):
    article = models.ForeignKey(
        Article,
        related_name="favorites",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name="favorites",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            "article",
            "user",
        )
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return str(self.article)
