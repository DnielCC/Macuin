"""Utilidades de sesión SQLAlchemy para la API."""

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def commit_or_raise(db: Session) -> None:
    """Confirma la transacción o devuelve 409 si hay violación de integridad."""
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="La operación no se pudo completar: conflicto de datos (duplicado o referencia inválida).",
        ) from exc
