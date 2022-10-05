import json

import pytest
from falcon import testing
from pytest_mock import MockerFixture

from graphql_api import app


@pytest.fixture
def client():
    return testing.TestClient(app.create_app())


@pytest.fixture
def sample_query():
    query = {
        "query": (
            "query listCountries($page: Int, $limit: Int){\n  countries(p"
            "age: $page, limit: $limit){\n    id\n   "
            " commonName\n    languages\n    location{\n      "
            "coordinates\n    }\n    unMember\n  }\n}"
        ),
        "variables": {
            "page": 0,
            "limit": 20
        },
        "operationName": "listCountries"}
    return json.dumps(query)


@pytest.mark.parametrize("route, expected_status_code", [
    ('/', 404),
    ('/graphql', 405),
    ('/admin', 404),
])
def test_routes_invalid(route, expected_status_code, client):
    resp = client.simulate_get(route)
    assert resp.status_code == expected_status_code


@pytest.mark.parametrize("route, expected_status_code", [
    ('/', 404),
    ('/graphql', 200),
    ('/admin', 404),
])
def test_routes_valid(route, expected_status_code, client, sample_query):
    client.simulate_request()
    resp = client.simulate_post(route, body=sample_query)
    assert resp.status_code == expected_status_code


def test_on_post_schema_exceptions(mocker: MockerFixture, monkeypatch, client,
                                   sample_query):
    schema_stub = mocker.async_stub("schema_stub")
    schema_stub.side_effect = Exception("Test exception")
    monkeypatch.setattr(
        app.schema,
        'execute_async',
        lambda *args, **kwargs: schema_stub())
    resp = client.simulate_post('/graphql', body=sample_query)
    assert resp.status_code == 500


def test_on_post(mocker: MockerFixture, monkeypatch, client, sample_query):
    schema_stub = mocker.async_stub("schema_stub")
    result_stub = mocker.stub("result_stub")
    result_stub.errors = None
    result_stub.data = {
        "data": "test data"
    }
    schema_stub.return_value = result_stub
    monkeypatch.setattr(app.schema, 'execute_async',
                        lambda *args, **kwargs: schema_stub())
    resp = client.simulate_post('/graphql', body=sample_query)
    assert resp.status_code == 200
