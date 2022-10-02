import logging

import requests

from graphql_api.config import country_data_api_url
from graphql_api.models import Country, Currency


def fetch_from_api() -> list:
    try:
        response = requests.get(country_data_api_url)
        return response.json()
    except requests.exceptions.RequestException:
        logging.error("Error occurred while fetching data from API")


def populate_database():
    if Country.objects.first() is not None:
        # if the database is already populated no need to populate it again
        return
    country_raw_data = fetch_from_api()
    logging.info("Collected data from API successfully")
    country_instances = []
    for idx, country_data in enumerate(country_raw_data):
        country = Country()
        country.area = country_data.get('area')
        country.common_name = country_data.get('name', {}).get('common')
        country.official_name = country_data.get('name', {}).get('official')
        country.un_member = country_data.get('unMember')
        country.independent = country_data.get('independent')
        country.region = country_data.get('region')
        country.subregion = country_data.get('subregion')
        latlong = country_data.get('latlng')
        # coordinate should be pushed in order longitude, latitude
        country.location = {
            "type": "Point",
            "coordinates": [latlong[1], latlong[0]]
        }
        # country.coordinates = {"lat": lat_long[0], "long": lat_long[1]}
        languages = country_data.get('languages')
        if languages:
            country.languages = list(languages.values())
        currency_raw = country_data.get('currencies')
        if currency_raw:
            currencies = []
            for short_name, details in currency_raw.items():
                currency = Currency(
                    short_name=short_name,
                    name=details['name'],
                    symbol=details.get('symbol')
                )
                currencies.append(currency)
            country.currencies = currencies
        country_instances.append(country)
    Country.objects.insert(country_instances, load_bulk=False)
    logging.info(f"Populated {idx + 1} documents")


if __name__ == '__main__':
    populate_database()
