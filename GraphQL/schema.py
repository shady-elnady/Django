from typing import cast

from Article.mutations.article_mutations import ArticleMutations
from Article.mutations.comment_mutations import CommentsMutations
from Article.queries import ArticleQuery
from graphene import Field, ObjectType, Schema
from graphene_django.debug import DjangoDebug
from Person.mutations import UsersMutations
from Person.queries import UsersQuery


class AppQuery(UsersQuery, ArticleQuery):
    """root query"""

    debug = Field(DjangoDebug, name="_debug")


class AppMutation(UsersMutations, ArticleMutations, CommentsMutations):
    """root mutation"""


schema = Schema(query=cast(ObjectType, AppQuery), mutation=AppMutation)
