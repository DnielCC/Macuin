"""Cliente HTTP hacia la API FastAPI (Macuin)."""

from __future__ import annotations

import os
from typing import Any, Optional

import requests


class ApiError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def _auth() -> tuple[str, str]:
    u = os.getenv("API_BASIC_USER", "alidaniel")
    p = os.getenv("API_BASIC_PASSWORD", "123456")
    return (u, p)


def _base() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


def _handle(r: requests.Response) -> Any:
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text or r.reason
        raise ApiError(r.status_code, str(detail))
    if r.status_code == 204 or not r.content:
        return None
    try:
        return r.json()
    except Exception:
        return r.text


class MacuinApi:
    def __init__(self):
        self.base = _base()
        self.auth = _auth()

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        r = requests.get(
            f"{self.base}{path}",
            params=params,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def post(self, path: str, json: Any = None) -> Any:
        r = requests.post(
            f"{self.base}{path}",
            json=json,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def put(self, path: str, json: Any = None) -> Any:
        r = requests.put(
            f"{self.base}{path}",
            json=json,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def patch(self, path: str, json: Any = None) -> Any:
        r = requests.patch(
            f"{self.base}{path}",
            json=json,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def delete(self, path: str) -> Any:
        r = requests.delete(f"{self.base}{path}", auth=self.auth, timeout=60)
        return _handle(r)

    def post_public(self, path: str, json: Any = None) -> Any:
        """Sin Basic (solo para /v1/auth/login)."""
        r = requests.post(f"{self.base}{path}", json=json, timeout=60)
        return _handle(r)


_api: Optional[MacuinApi] = None


def get_api() -> MacuinApi:
    global _api
    if _api is None:
        _api = MacuinApi()
    return _api
