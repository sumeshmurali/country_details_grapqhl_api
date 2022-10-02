import pytest
import mongoengine

from graphql_api.config import mongodb_url
from graphql_api import models


@pytest.fixture
def connection():
    mongoengine.connect("testdb", host=mongodb_url, alias="test_connection")
    yield
    mongoengine.disconnect(alias="test_connection")


def test_if_production():
    assert "mongomock" in mongodb_url, \
        f"Production URL ({mongodb_url}) is used for testing"


@pytest.mark.parametrize("name", ["", None, 1234, 39.2, "1234"])
def test_currency_model_name_invalid(name):
    test_currency = models.Currency()
    test_currency.short_name = "USD"
    test_currency.name = name
    with pytest.raises(mongoengine.ValidationError):
        test_currency.validate()


@pytest.mark.parametrize("name", [
    "Tongan paʻanga",
    "United States dollar",
    "Indian rupee"
])
def test_currency_model_name_valid(name):
    test_currency = models.Currency()
    test_currency.short_name = "USD"
    test_currency.name = name
    test_currency.validate()


@pytest.mark.parametrize("name", ["", None, 1234, 39.2, "1234"])
def test_currency_model_short_name_invalid(name):
    test_currency = models.Currency()
    test_currency.name = "USD"
    test_currency.short_name = name
    with pytest.raises(mongoengine.ValidationError):
        test_currency.validate()


@pytest.mark.parametrize("name", ["USD", "INR", "TOP"])
def test_currency_model_short_name_valid(name):
    test_currency = models.Currency()
    test_currency.name = "USD"
    test_currency.short_name = name
    test_currency.validate()


@pytest.mark.parametrize("coordinates", [
    (80, 181),
    (120, 90),
    (-91, 190),
    (-80, -190),
    (80.00, 1000),
    (None, None),
    ("", ""),
    (80, None),
    (80, ""),
    ("", 180),
    (None, 170)
])
def test_country_model_coordinates_invalid(coordinates):
    test_country = models.Country()
    test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.independent = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = coordinates[::-1]
    with pytest.raises(mongoengine.ValidationError):
        test_country.validate()


@pytest.mark.parametrize("coordinates", [
    (80, 180),
    (67, 90),
    (-90, 100),
    (-80, -110),
    (80.00, 20),
    (0.0, 100),
    (10, 0.0)
])
def test_country_model_coordinates_valid(coordinates):
    test_country = models.Country()
    test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.independent = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = coordinates[::-1]
    test_country.validate()


@pytest.mark.parametrize("value", [None, "a", 123, Exception])
def test_country_boolean_fields_invalid(value):
    test_country = models.Country()
    test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = [40.7128, 74.0060]
    # testing independence field
    test_country.independent = value
    with pytest.raises(mongoengine.ValidationError):
        test_country.validate()
    # testing un member field
    test_country.independent = False
    test_country.un_member = value
    with pytest.raises(mongoengine.ValidationError):
        test_country.validate()


@pytest.mark.parametrize("value", [True, False])
def test_country_boolean_fields_valid(value):
    test_country = models.Country()
    test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = [40.7128, 74.0060]
    # testing independence field
    test_country.independent = value
    test_country.validate()
    # testing un member field
    test_country.independent = False
    test_country.un_member = value
    test_country.validate()


@pytest.mark.parametrize("value", ["", None, 123, "1234", 20.2, []])
def test_country_string_fields_invalid(value):
    test_country = models.Country()
    test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = [40.7128, 74.0060]
    test_country.independent = False
    # testing common name
    test_country.common_name = value
    with pytest.raises(mongoengine.ValidationError):
        test_country.validate()
    test_country.common_name = "Test Country"
    # testing official name
    test_country.official_name = value
    with pytest.raises(mongoengine.ValidationError):
        test_country.validate()
    test_country.official_name = "Test Country"
    # testing region
    test_country.region = value
    with pytest.raises(mongoengine.ValidationError):
        test_country.validate()


@pytest.mark.parametrize("value", ["Test String"])
def test_country_string_fields_valid(value):
    test_country = models.Country()
    test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = [40.7128, 74.0060]
    test_country.independent = False
    # testing common name
    test_country.common_name = value
    test_country.validate()
    test_country.common_name = "Test Country"
    # testing official name
    test_country.official_name = value
    test_country.validate()
    test_country.official_name = "Test Country"
    # testing region
    test_country.region = value
    test_country.validate()


@pytest.mark.parametrize("value", ["Test", None, False, ""])
def test_country_int_fields_invalid(value):
    test_country = models.Country()
    # test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = [40.7128, 74.0060]
    test_country.independent = False
    # testing area
    test_country.area = value
    with pytest.raises(mongoengine.ValidationError):
        test_country.validate()


@pytest.mark.parametrize("value", [1, 0, 1000, 20.4])
def test_country_int_fields_valid(value):
    test_country = models.Country()
    # test_country.area = 500
    test_country.common_name = "Test Country"
    test_country.official_name = "Test Country"
    test_country.un_member = False
    test_country.region = "Test Region"
    test_country.subregion = None
    test_country.location = [40.7128, 74.0060]
    test_country.independent = False
    # testing area
    test_country.area = value
    test_country.validate()
