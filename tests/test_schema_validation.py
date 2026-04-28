"""
test_schema_validation.py
--------------------------
JSON schema contract tests.
Ensures API responses conform to expected data contracts —
critical for catching breaking changes in distributed microservices.
"""

import allure
import pytest

from src.validators.response_validator import validate

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id":       {"type": "integer"},
        "name":     {"type": "string", "minLength": 1},
        "username": {"type": "string", "minLength": 1},
        "email":    {"type": "string", "format": "email"},
        "phone":    {"type": "string"},
        "website":  {"type": "string"},
        "address": {
            "type": "object",
            "required": ["street", "city", "zipcode"],
            "properties": {
                "street":  {"type": "string"},
                "city":    {"type": "string"},
                "zipcode": {"type": "string"},
            }
        },
        "company": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string"},
            }
        }
    }
}

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id":     {"type": "integer"},
        "title":  {"type": "string", "minLength": 1},
        "body":   {"type": "string"},
    }
}


@allure.suite("Schema Validation")
@allure.feature("Contract testing — response schema")
class TestSchemaValidation:

    @allure.title("GET /users/1 response matches User schema contract")
    def test_user_response_matches_schema(self, api_client):
        response = api_client.get("/users/1")
        (validate(response)
            .status_is(200)
            .matches_schema(USER_SCHEMA))

    @allure.title("GET /posts/1 response matches Post schema contract")
    def test_post_response_matches_schema(self, api_client):
        response = api_client.get("/posts/1")
        (validate(response)
            .status_is(200)
            .matches_schema(POST_SCHEMA))

    @pytest.mark.parametrize("user_id", [1, 2, 3])
    @allure.title("Schema contract holds across multiple user records")
    def test_schema_consistent_across_users(self, api_client, user_id):
        response = api_client.get(f"/users/{user_id}")
        validate(response).status_is(200).matches_schema(USER_SCHEMA)
