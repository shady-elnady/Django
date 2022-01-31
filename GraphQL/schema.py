from typing import cast

from Articles.mutations.article_mutations import ArticleMutations
from Articles.mutations.comment_mutations import CommentsMutations
from Articles.queries import ArticleQuery
from graphene import Field, ObjectType, Schema
from graphene_django.debug import DjangoDebug
from Persons.mutations import UsersMutations
from Persons.queries import UsersQuery


class AppQuery(UsersQuery, ArticleQuery):
    """root query"""

    debug = Field(DjangoDebug, name="_debug")


class AppMutation(UsersMutations, ArticleMutations, CommentsMutations):
    """root mutation"""


schema = Schema(query=cast(ObjectType, AppQuery), mutation=AppMutation)
