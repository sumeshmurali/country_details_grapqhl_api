import mongoengine

from graphql_api.config import mongodb_url, mongodb_db_name
from graphql_api import validators

mongoengine.connect(mongodb_db_name, host=mongodb_url)


class Currency(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(
        required=True,
        validation=validators.validate_string,
        min_length=1,
        max_length=100,
    )
    symbol = mongoengine.StringField(
        required=True,
        validation=validators.validate_string,
        min_length=1,
        max_length=5
    )
    short_name = mongoengine.StringField(
        required=True,
        validation=validators.validate_string,
        min_length=1,
        max_length=5,
    )


class Country(mongoengine.Document):
    common_name = mongoengine.StringField(
        required=True,
        validation=validators.validate_string,
        min_length=1,
        max_length=100,
    )
    official_name = mongoengine.StringField(
        required=True,
        validation=validators.validate_string,
        min_length=1,
        max_length=100
    )
    independent = mongoengine.BooleanField(
        required=True,
        validation=validators.validate_boolean_values
    )
    un_member = mongoengine.BooleanField(
        required=True,
        validation=validators.validate_boolean_values
    )
    languages = mongoengine.ListField(
        mongoengine.StringField(
            validation=validators.validate_string,
            min_length=1,
            max_length=100
        )
    )
    # longitude, latitude format
    location = mongoengine.PointField(
        required=True,
        validation=validators.validate_coordinates
    )
    area = mongoengine.IntField(
        required=True,
        validation=validators.validate_numbers,
        # a country with area less than 1 is not logical
        min_value=1
    )
    region = mongoengine.StringField(
        required=True,
        validation=validators.validate_string,
        min_length=1,
        max_length=100,

    )
    subregion = mongoengine.StringField(
        validation=validators.validate_string,
        min_length=1,
        max_length=100,
    )
    currencies = mongoengine.ListField(
        mongoengine.EmbeddedDocumentField(Currency)
    )
    meta = {
        "indexes": [
            "languages",
        ]
    }
