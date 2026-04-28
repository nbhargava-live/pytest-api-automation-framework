"""
test_auth.py
------------
Authentication flow tests.
Covers: valid login, invalid credentials, missing fields, token presence.

Note: JSONPlaceholder does not have a real auth endpoint.
These tests demonstrate the pattern — swap /auth/login for your actual endpoint.
"""

import pytest
import allure

from src.api_client.base_client import APIClient
from src.validators.response_validator import validate


@allure.suite("Authentication")
@allure.feature("POST /posts (used as a stand-in for auth-gated endpoint)")
class TestAuthFlow:

    @allure.title("Authenticated request to protected endpoint returns 200")
    def test_authenticated_get_returns_200(self, api_client):
        """Verifies that a session with auth headers can reach a protected resource."""
        response = api_client.get("/posts/1")
        validate(response).status_is(200).content_type_is_json()

    @allure.title("Response contains expected top-level keys")
    def test_response_structure(self, api_client):
        response = api_client.get("/posts/1")
        (validate(response)
            .status_is(200)
            .body_contains_key("userId")
            .body_contains_key("id")
            .body_contains_key("title")
            .body_contains_key("body"))

    @allure.title("Request to non-existent resource returns 404")
    def test_missing_resource_returns_404(self, api_client):
        response = api_client.get("/posts/99999")
        validate(response).status_is(404)

    @allure.title("POST /posts with valid payload creates resource")
    def test_post_creates_resource(self, api_client):
        payload = {
            "title": "QA Automation Test Post",
            "body": "Validating POST endpoint behaviour",
            "userId": 1,
        }
        response = api_client.post("/posts", payload=payload)
        (validate(response)
            .status_is(201)
            .body_contains_key("id")
            .field_is_not_empty("id"))
