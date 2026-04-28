"""
response_validator.py
---------------------
Reusable assertion helpers for API response validation.
Covers: status codes, JSON schema, headers, response time SLAs,
and field-level assertions with clear failure messages.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import jsonschema
import requests

logger = logging.getLogger(__name__)


class ResponseValidator:
    """Fluent validator — chain assertions for readable test code."""

    def __init__(self, response: requests.Response):
        self.response = response
        self._json: Optional[Dict] = None

    # ── Status ──────────────────────────────────────────────────────────────

    def status_is(self, expected: int) -> "ResponseValidator":
        actual = self.response.status_code
        assert actual == expected, (
            f"Expected HTTP {expected}, got {actual}.\n"
            f"URL: {self.response.url}\n"
            f"Body: {self.response.text[:300]}"
        )
        logger.info(f"Status check passed: {actual}")
        return self

    def status_in(self, expected: List[int]) -> "ResponseValidator":
        actual = self.response.status_code
        assert actual in expected, (
            f"Expected one of {expected}, got {actual}.\nURL: {self.response.url}"
        )
        return self

    # ── Body ────────────────────────────────────────────────────────────────

    def body_contains_key(self, key: str) -> "ResponseValidator":
        data = self._get_json()
        assert key in data, f"Key '{key}' not found in response. Keys present: {list(data.keys())}"
        return self

    def field_equals(self, key: str, expected: Any) -> "ResponseValidator":
        data = self._get_json()
        actual = data.get(key)
        assert actual == expected, (
            f"Field '{key}': expected '{expected}', got '{actual}'"
        )
        return self

    def field_is_not_empty(self, key: str) -> "ResponseValidator":
        data = self._get_json()
        value = data.get(key)
        assert value not in (None, "", [], {}), (
            f"Field '{key}' is empty or null"
        )
        return self

    def list_is_not_empty(self, key: Optional[str] = None) -> "ResponseValidator":
        data = self._get_json()
        target = data.get(key) if key else data
        assert isinstance(target, list) and len(target) > 0, (
            f"Expected non-empty list at '{key}', got: {target}"
        )
        return self

    # ── Schema ───────────────────────────────────────────────────────────────

    def matches_schema(self, schema: Dict) -> "ResponseValidator":
        data = self._get_json()
        try:
            jsonschema.validate(instance=data, schema=schema)
            logger.info("Schema validation passed")
        except jsonschema.ValidationError as e:
            raise AssertionError(
                f"Schema validation failed: {e.message}\n"
                f"Failed at path: {list(e.absolute_path)}"
            )
        return self

    # ── Headers ──────────────────────────────────────────────────────────────

    def header_present(self, header: str) -> "ResponseValidator":
        assert header.lower() in {k.lower() for k in self.response.headers}, (
            f"Expected header '{header}' not found in response headers."
        )
        return self

    def content_type_is_json(self) -> "ResponseValidator":
        ct = self.response.headers.get("Content-Type", "")
        assert "application/json" in ct, (
            f"Expected Content-Type: application/json, got: {ct}"
        )
        return self

    # ── Performance ───────────────────────────────────────────────────────────

    def response_time_under(self, max_ms: int) -> "ResponseValidator":
        actual_ms = self.response.elapsed.total_seconds() * 1000
        assert actual_ms < max_ms, (
            f"Response time {actual_ms:.0f}ms exceeded SLA of {max_ms}ms"
        )
        logger.info(f"Response time: {actual_ms:.0f}ms (SLA: {max_ms}ms)")
        return self

    # ── Internal ─────────────────────────────────────────────────────────────

    def _get_json(self) -> Dict:
        if self._json is None:
            try:
                self._json = self.response.json()
            except json.JSONDecodeError:
                raise AssertionError(
                    f"Response body is not valid JSON.\nBody: {self.response.text[:300]}"
                )
        return self._json


def validate(response: requests.Response) -> ResponseValidator:
    """Factory shorthand — use in tests as: validate(response).status_is(200)"""
    return ResponseValidator(response)
