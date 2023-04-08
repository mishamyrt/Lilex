"""Feature name utils"""
from __future__ import annotations

from re import match, search


def name_from_code(content: str) -> str | None:
    result = search(r'Name:(.*)', content)
    try:
        return result.group(1).strip()
    except AttributeError:
        return None

def feature_prefix(name: str) -> str | None:
    result = match(r'([a-z]+)', name)
    try:
        return result.group(1)
    except AttributeError:
        return None
