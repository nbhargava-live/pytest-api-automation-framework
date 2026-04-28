"""
data_loader.py
--------------
Utilities for loading test data from JSON and CSV fixture files.
Supports data-driven testing patterns with pytest.mark.parametrize.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)

FIXTURES_DIR = Path(__file__).parent.parent.parent / "tests" / "fixtures"


def load_json(filename: str) -> Union[Dict, List]:
    """Load a JSON fixture file from the tests/fixtures directory."""
    path = FIXTURES_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    logger.debug(f"Loaded JSON fixture: {filename}")
    return data


def load_csv(filename: str) -> List[Dict[str, str]]:
    """
    Load a CSV fixture and return a list of row dicts.
    First row is treated as headers.
    """
    path = FIXTURES_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    logger.debug(f"Loaded CSV fixture: {filename} ({len(rows)} rows)")
    return rows


def parametrize_from_json(filename: str, key: str) -> List[Any]:
    """
    Extract a list from a JSON fixture for use with pytest.mark.parametrize.

    Usage:
        @pytest.mark.parametrize("payload", parametrize_from_json("users.json", "create_cases"))
        def test_create_user(payload): ...
    """
    data = load_json(filename)
    if isinstance(data, dict):
        return data.get(key, [])
    return data
