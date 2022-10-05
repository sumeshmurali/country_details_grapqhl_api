import os

mongodb_db_name = os.getenv('env_mongodb_dbname', 'testdb')
mongodb_url = os.getenv('env_mongodb_url', 'mongomock://localhost')
country_data_api_url = 'https://restcountries.com/v3.1/all'
