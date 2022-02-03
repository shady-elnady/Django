from django.db import models
from GraphQL.models import BaseModel, BaseModelName
from djongo.models import ArrayField
from Persons.models import User


# Create your models here.


MAX_LENGTH = 100


class Tag(BaseModelName):
    pass


class Article(BaseModel):
    title = models.CharField(max_length=MAX_LENGTH, blank=False, null=False)
    slug = models.SlugField(
        max_length=MAX_LENGTH, blank=False, null=False, unique=True,
    )
    description = models.TextField(null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    # TODO Djongo Array Field
    tags = ArrayField(
        model_container=Tag,
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articles",
    )


class Comment(BaseModel):
    body = models.TextField()
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE,
    )


class FavoriteArticles(BaseModel):
    article = models.ForeignKey(
        Article, related_name="favorites", on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User, related_name="favorites", on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            "article",
            "user",
        )
