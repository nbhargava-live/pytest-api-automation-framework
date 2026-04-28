"""
conftest.py
-----------
Shared pytest fixtures available across all test modules.
Handles: API client setup, auth token injection, environment config.
"""

import os
import pytest
from dotenv import load_dotenv

from src.api_client.base_client import APIClient

load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    url = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    return url


@pytest.fixture(scope="session")
def api_client(base_url) -> APIClient:
    """Session-scoped API client — shared across all tests for efficiency."""
    client = APIClient(
        base_url=base_url,
        headers={"X-Framework": "pytest-api-automation"},
        timeout=30,
        max_retries=3,
    )
    return client


@pytest.fixture(scope="session")
def auth_token(api_client) -> str:
    """
    Obtain and cache a Bearer token for the test session.
    Replace the payload/endpoint with your actual auth service details.
    """
    response = api_client.post("/auth/login", payload={
        "username": os.getenv("API_USERNAME", "test_user"),
        "password": os.getenv("API_PASSWORD", "test_password"),
    })
    # For JSONPlaceholder (demo), skip real auth and return a mock token
    if response.status_code == 404:
        return "demo-token-not-required"
    token = response.json().get("token", "")
    api_client.set_auth_token(token)
    return token


@pytest.fixture(scope="function")
def sample_user_payload() -> dict:
    return {
        "name": "Nikita Test User",
        "username": "nikita_qa",
        "email": "test@example.com",
        "phone": "416-555-0100",
        "website": "nikita-qa.dev",
    }
