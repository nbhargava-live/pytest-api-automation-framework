"""
base_client.py
--------------
Core HTTP client for the API automation framework.
Wraps the requests library with retry logic, session management,
structured logging, and response timing.
"""

import logging
import time
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class APIClient:
    """
    Thread-safe HTTP client with:
    - Automatic retries with exponential backoff
    - Persistent session with shared headers
    - Request/response logging for Allure reports
    - Response time tracking
    """

    def __init__(self, base_url: str, headers: Optional[Dict] = None,
                 timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = self._build_session(max_retries)
        if headers:
            self.session.headers.update(headers)
        logger.info(f"APIClient initialised — base_url={self.base_url}")

    def _build_session(self, max_retries: int) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        return session

    def set_auth_token(self, token: str) -> None:
        """Set Bearer token on the session — persists across all subsequent requests."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.debug("Bearer token applied to session")

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, payload: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, json=payload, **kwargs)

    def put(self, endpoint: str, payload: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request("PUT", endpoint, json=payload, **kwargs)

    def patch(self, endpoint: str, payload: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request("PATCH", endpoint, json=payload, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start = time.perf_counter()
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            self._log_response(method, url, response, elapsed)
            return response
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error — {method} {url}: {e}")
            raise
        except requests.exceptions.Timeout:
            logger.error(f"Timeout after {self.timeout}s — {method} {url}")
            raise

    def _log_response(self, method: str, url: str, response: requests.Response,
                      elapsed_ms: float) -> None:
        level = logging.WARNING if response.status_code >= 400 else logging.INFO
        logger.log(level,
                   f"{method} {url} → {response.status_code} ({elapsed_ms}ms)")
        if response.status_code >= 400:
            logger.debug(f"Response body: {response.text[:500]}")
