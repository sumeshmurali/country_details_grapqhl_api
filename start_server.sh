# TODO find a better implementation for populating database
# populating database
python populate_db.py

uvicorn --host 0.0.0.0 --port 80 graphql_api.app:app