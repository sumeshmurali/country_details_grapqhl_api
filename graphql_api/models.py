import mongoengine
import haversine

from graphql_api.config import mongodb_url, mongodb_db_name
from graphql_api import validators

mongoengine.connect(mongodb_db_name, host=mongodb_url)


class Currency(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(required=True, validation=validators.validate_string)
    symbol = mongoengine.StringField()
    short_name = mongoengine.StringField(required=True, validation=validators.validate_string)


class Country(mongoengine.Document):
    # TODO add length validation - necessary to not input too large fields
    common_name = mongoengine.StringField(required=True, validation=validators.validate_string)
    official_name = mongoengine.StringField(required=True, validation=validators.validate_string)
    independent = mongoengine.BooleanField(validation=validators.validate_boolean_values)
    un_member = mongoengine.BooleanField(required=True, validation=validators.validate_boolean_values)
    # TODO add validators for languages
    languages = mongoengine.DictField()
    # longitude, latitude format
    coordinates = mongoengine.PointField(required=True, validation=validators.validate_coordinates)
    area = mongoengine.IntField(required=True, validation=validators.validate_numbers)
    region = mongoengine.StringField(required=True, validation=validators.validate_string)
    subregion = mongoengine.StringField(validation=validators.validate_string)
    currencies = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Currency))

    def is_near(self, lat: float, long: float, range_: float) -> bool:
        # TODO use mongodb distance calculation features here
        distance = haversine.haversine(self.coordinates, (lat, long))
        return distance < range_
