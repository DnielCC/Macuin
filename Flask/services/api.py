"""Cliente HTTP hacia la API FastAPI (Macuin)."""

from __future__ import annotations

import json
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


def _decode_json_bytes(raw: bytes) -> Any:
    """Decodifica JSON siempre como UTF-8 (evita ?? por charset mal inferido en r.json())."""
    return json.loads(raw.decode("utf-8"))


def _looks_json_body(raw: bytes) -> bool:
    if not raw:
        return False
    c = raw.lstrip()[:1]
    return c in (b"{", b"[")


def _handle(r: requests.Response) -> Any:
    ct = (r.headers.get("Content-Type") or "").lower()
    is_json = "application/json" in ct or _looks_json_body(r.content or b"")

    if r.status_code >= 400:
        detail: str
        if is_json and r.content:
            try:
                payload = _decode_json_bytes(r.content)
                if isinstance(payload, dict):
                    d = payload.get("detail")
                    detail = str(d) if d is not None else (r.text or r.reason)
                else:
                    detail = str(payload)
            except Exception:
                detail = r.text or r.reason
        else:
            detail = r.text or r.reason
        raise ApiError(r.status_code, str(detail))

    if r.status_code == 204 or not r.content:
        return None

    if is_json:
        try:
            return _decode_json_bytes(r.content)
        except (UnicodeDecodeError, json.JSONDecodeError):
            r.encoding = "utf-8"
            return r.json()

    r.encoding = "utf-8"
    return r.text


def _json_payload_bytes(payload: Any) -> Optional[bytes]:
    """Serializa JSON en UTF-8 sin \\uXXXX (acentos legibles en wire y en logs)."""
    if payload is None:
        return None
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


class MacuinApi:
    def __init__(self):
        self.base = _base()
        self.auth = _auth()

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        r = requests.get(
            f"{self.base}{path}",
            params=params or None,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def post(self, path: str, json: Any = None) -> Any:
        body = _json_payload_bytes(json)
        headers = {"Content-Type": "application/json; charset=utf-8"} if body is not None else {}
        r = requests.post(
            f"{self.base}{path}",
            data=body,
            headers=headers,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def put(self, path: str, json: Any = None) -> Any:
        body = _json_payload_bytes(json)
        headers = {"Content-Type": "application/json; charset=utf-8"} if body is not None else {}
        r = requests.put(
            f"{self.base}{path}",
            data=body,
            headers=headers,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def patch(self, path: str, json: Any = None) -> Any:
        body = _json_payload_bytes(json)
        headers = {"Content-Type": "application/json; charset=utf-8"} if body is not None else {}
        r = requests.patch(
            f"{self.base}{path}",
            data=body,
            headers=headers,
            auth=self.auth,
            timeout=60,
        )
        return _handle(r)

    def delete(self, path: str) -> Any:
        r = requests.delete(f"{self.base}{path}", auth=self.auth, timeout=60)
        return _handle(r)

    def post_public(self, path: str, json: Any = None) -> Any:
        """Sin Basic (solo para /v1/auth/login)."""
        body = _json_payload_bytes(json)
        headers = {"Content-Type": "application/json; charset=utf-8"} if body is not None else {}
        r = requests.post(f"{self.base}{path}", data=body, headers=headers, timeout=60)
        return _handle(r)


_api: Optional[MacuinApi] = None


def get_api() -> MacuinApi:
    global _api
    if _api is None:
        _api = MacuinApi()
    return _api
