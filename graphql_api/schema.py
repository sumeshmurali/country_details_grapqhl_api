import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from graphql_api.models import Country as CountryModel


class Country(MongoengineObjectType):
    class Meta:
        model = CountryModel
        interfaces = (Node, )


class Query(graphene.ObjectType):
    node = Node.Field()
    all_countries = MongoengineConnectionField(Country)
    country = graphene.Field(Country)


schema = graphene.Schema(query=Query, types=[Country])
