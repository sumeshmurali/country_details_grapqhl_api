import base64

import graphene
from graphene import String
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from mongoengine import ValidationError

from graphql_api.models import Country as CountryModel
from graphql_api.validators import validate_coordinates


class Country(MongoengineObjectType):
    class Meta:
        model = CountryModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    node = Node.Field()
    countries = graphene.List(
        graphene.NonNull(Country),
        page=graphene.Int(default_value=0, ),
        limit=graphene.Int(default_value=20)
    )
    country = graphene.Field(Country, id=String(required=True))
    countries_by_language = graphene.List(
        Country,
        language=String(required=True),
        page=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=20)
    )
    countries_near_location = graphene.List(
        Country,
        lat=graphene.Float(required=True),
        long=graphene.Float(required=True),
        range=graphene.Int(required=True),
        page=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=20)
    )

    @staticmethod
    def resolve_country(root, info, id: str):
        if not id:
            raise GraphQLError("ID should not be empty")

        try:
            id_decoded = base64.b64decode(id).decode().split(":")[-1]
        except Exception:
            raise GraphQLError("Incorrect ID")

        results = CountryModel.objects(pk=id_decoded)
        if not results:
            raise GraphQLError("Incorrect ID")
        return results.first()

    @staticmethod
    def resolve_countries(root, info, page=0, limit=20):
        if page < 0 or not 10 <= limit <= 50:
            # page should not be less than zero and also limits values are
            # to be limited to not let a user collect more data than they
            # need to
            raise GraphQLError("Incorrect pagination parameters")
        results = CountryModel.objects[page * limit:page * limit + limit]
        return results

    @staticmethod
    def resolve_countries_by_language(
            root,
            info,
            language: str,
            page: int = 0,
            limit: int = 20
    ):
        if page < 0 or not 10 <= limit <= 50:
            # page should not be less than zero and also limits values are
            # to be limited to not let a user collect more data than they
            # need to
            raise GraphQLError("Incorrect pagination parameters")
        results = CountryModel.objects(
            languages=language
        )
        # limiting results
        results = results[page * limit:page * limit + limit]
        return results

    @staticmethod
    def resolve_countries_near_location(
            root,
            info,
            lat: int,
            long: int,
            range: int,
            page: int = 0,
            limit: int = 20
    ):
        if page < 0 or not 10 <= limit <= 50:
            # page should not be less than zero and also limits values are
            # to be limited to not let a user collect more data than they
            # need to
            raise GraphQLError("Incorrect pagination parameters")
        try:
            validate_coordinates([long, lat])
        except ValidationError:
            raise GraphQLError("Incorrect parameters for coordinates")
        # mongodb features geospatial queries which can be used to
        # collect nearby locations of a coordinate
        results = CountryModel.objects(
            location__near=[long, lat],
            location__max_distance=range
        )
        # limiting results
        results = results[page * limit:page * limit + limit]
        return results


class UpdateCountry(graphene.Mutation):
    class Arguments:
        id_ = graphene.String(required=True)
        independent = graphene.Boolean()
        un_member = graphene.Boolean()
        area = graphene.Int()
        languages = graphene.List(graphene.String)
        language = graphene.String()

    success = graphene.Boolean()
    country = graphene.Field(Country)

    @staticmethod
    def mutate(
            root,
            info,
            id_: str,
            independent: bool = None,
            un_member: bool = None,
            area: int = None,
            languages: list = None,
            language: str = None
    ):
        try:
            id_decoded = base64.b64decode(id_).decode().split(":")[-1]
        except Exception:
            raise GraphQLError("Incorrect ID")
        if not CountryModel.objects(pk=id_decoded).first():
            raise GraphQLError("Incorrect ID")

        # Its possible multiple fields can be updated once and
        # update_fields allows us to update multiple params
        update_fields = {}
        if independent is not None:
            update_fields['set__independent'] = independent
        if un_member is not None:
            update_fields['set__un_member'] = un_member
        if area is not None:
            update_fields['set__area'] = area
        if languages:
            update_fields['set__languages'] = languages
        if language:
            update_fields['push__languages'] = language

        if not update_fields:
            raise GraphQLError("No update parameters provided")

        CountryModel.objects(pk=id_decoded).update_one(**update_fields)
        country = CountryModel.objects(pk=id_decoded).first()
        success = True
        return UpdateCountry(country=country, success=success)


class Mutation(graphene.ObjectType):
    update_country = UpdateCountry.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[Country])
