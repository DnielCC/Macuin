"""Validaciones de entrada para formularios Flask."""

import re
from typing import Optional, Tuple


def _err(msg: str) -> Tuple[bool, str]:
    return False, msg


def _ok() -> Tuple[bool, str]:
    return True, ""


def require_non_empty(value: Optional[str], label: str) -> Tuple[bool, str]:
    if value is None or not str(value).strip():
        return _err(f"{label} es obligatorio.")
    return _ok()


def validate_email(email: Optional[str]) -> Tuple[bool, str]:
    if not email or not str(email).strip():
        return _err("El correo es obligatorio.")
    e = str(email).strip().lower()
    if len(e) > 120:
        return _err("El correo es demasiado largo.")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e):
        return _err("El formato del correo no es válido.")
    return True, e


def validate_phone(phone: Optional[str]) -> Tuple[bool, str]:
    if phone is None or not str(phone).strip():
        return True, ""
    p = re.sub(r"\s+", "", str(phone))
    if len(p) > 30:
        return _err("El teléfono es demasiado largo.")
    if not re.match(r"^[\d+\-().]{7,30}$", p):
        return _err("El teléfono solo debe contener dígitos y símbolos permitidos.")
    return True, p


def validate_int(value, label: str, min_v: int = 1, max_v: Optional[int] = None) -> Tuple[bool, str, Optional[int]]:
    try:
        n = int(value)
    except (TypeError, ValueError):
        return False, f"{label} debe ser un número entero.", None
    if n < min_v:
        return False, f"{label} debe ser mayor o igual que {min_v}.", None
    if max_v is not None and n > max_v:
        return False, f"{label} no puede ser mayor que {max_v}.", None
    return True, "", n


def validate_float(value, label: str, min_v: float = 0.0) -> Tuple[bool, str, Optional[float]]:
    try:
        x = float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return False, f"{label} debe ser un número.", None
    if x < min_v:
        return False, f"{label} debe ser mayor o igual que {min_v}.", None
    return True, "", x


def validate_sku(sku: Optional[str]) -> Tuple[bool, str]:
    ok, msg = require_non_empty(sku, "SKU / código")
    if not ok:
        return ok, msg
    s = str(sku).strip()
    if len(s) > 50:
        return _err("El SKU no puede superar 50 caracteres.")
    if not re.match(r"^[A-Za-z0-9._\-]+$", s):
        return _err("El SKU solo permite letras, números, punto, guion y guion bajo.")
    return True, s


def validate_password_plain(pw: Optional[str], min_len: int = 6) -> Tuple[bool, str]:
    if not pw or len(str(pw)) < min_len:
        return _err(f"La contraseña debe tener al menos {min_len} caracteres.")
    if len(str(pw)) > 128:
        return _err("La contraseña es demasiado larga.")
    return True, str(pw)


def validate_cp_mx(cp: Optional[str], label: str = "Código postal") -> Tuple[bool, str]:
    if not cp or not str(cp).strip():
        return _err(f"{label} es obligatorio.")
    c = re.sub(r"\s+", "", str(cp))
    if not re.match(r"^\d{5}$", c):
        return _err(f"{label} debe tener 5 dígitos.")
    return True, c


def validate_short_text(value: Optional[str], label: str, max_len: int, required: bool = True) -> Tuple[bool, str]:
    if value is None or not str(value).strip():
        if required:
            return _err(f"{label} es obligatorio.")
        return True, ""
    s = str(value).strip()
    if len(s) > max_len:
        return _err(f"{label} no puede superar {max_len} caracteres.")
    return True, s
