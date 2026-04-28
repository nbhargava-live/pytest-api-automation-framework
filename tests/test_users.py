"""
test_users.py
-------------
Test suite for the Users API endpoint.
Covers: GET list, GET by ID, POST create, schema validation,
response time SLA, and negative/error scenarios.

Uses: https://jsonplaceholder.typicode.com (public mock API — no auth needed)
Replace with your target API base URL in .env
"""

import pytest
import allure

from src.validators.response_validator import validate


@allure.suite("Users API")
@allure.feature("GET /users")
class TestGetUsers:

    @allure.title("GET /users returns 200 and non-empty list")
    def test_get_all_users_returns_200(self, api_client):
        response = api_client.get("/users")
        (validate(response)
            .status_is(200)
            .content_type_is_json()
            .list_is_not_empty()
            .response_time_under(3000))

    @allure.title("GET /users response time within SLA")
    def test_get_users_response_time_sla(self, api_client):
        response = api_client.get("/users")
        validate(response).response_time_under(2000)


@allure.suite("Users API")
@allure.feature("GET /users/{id}")
class TestGetUserById:

    @allure.title("GET /users/1 returns correct user fields")
    def test_get_user_by_valid_id(self, api_client):
        response = api_client.get("/users/1")
        (validate(response)
            .status_is(200)
            .body_contains_key("id")
            .body_contains_key("name")
            .body_contains_key("email")
            .field_equals("id", 1)
            .field_is_not_empty("name")
            .field_is_not_empty("email"))

    @allure.title("GET /users/9999 returns 404 for unknown ID")
    def test_get_user_by_invalid_id_returns_404(self, api_client):
        response = api_client.get("/users/9999")
        validate(response).status_is(404)


@allure.suite("Users API")
@allure.feature("POST /users")
class TestCreateUser:

    @allure.title("POST /users with valid payload returns 201")
    def test_create_user_returns_201(self, api_client, sample_user_payload):
        response = api_client.post("/users", payload=sample_user_payload)
        (validate(response)
            .status_is(201)
            .body_contains_key("id")
            .field_is_not_empty("id"))

    @allure.title("POST /users response echoes submitted name")
    def test_create_user_response_echoes_name(self, api_client, sample_user_payload):
        response = api_client.post("/users", payload=sample_user_payload)
        validate(response).status_is(201).field_equals("name", sample_user_payload["name"])

    @pytest.mark.parametrize("user_id", [1, 2, 3, 5, 10])
    @allure.title("GET /users/{id} — parametrized across multiple IDs")
    def test_get_multiple_users_by_id(self, api_client, user_id):
        response = api_client.get(f"/users/{user_id}")
        (validate(response)
            .status_is(200)
            .field_equals("id", user_id))
