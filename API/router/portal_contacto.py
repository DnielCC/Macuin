"""Lectura y marca leída de mensajes de contacto del portal Laravel (tabla contact_messages)."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database.contact_messages import CustomerContactMessage
from database.db import get_db
from database.db_utils import commit_or_raise
from models.contact_portal_admin import ContactPortalAdminReply
from security.auth import varificar_peticion

router_portal_contacto = APIRouter(prefix="/v1/portal-contacto", tags=["Contacto portal"])


def _serializar(m: CustomerContactMessage) -> dict:
    def _iso(dt):
        if dt is None:
            return None
        if getattr(dt, "tzinfo", None) is None:
            return dt.isoformat()
        return dt.isoformat()

    return {
        "id": int(m.id),  # type: ignore
        "laravel_contact_message_id": int(m.id),  # type: ignore
        "nombre": m.name,
        "email": m.email,
        "telefono": m.phone,
        "asunto": m.subject,
        "mensaje": m.message,
        "admin_reply": m.admin_reply,
        "replied_at": _iso(m.replied_at) if m.replied_at else None, # type: ignore
        "is_read": bool(m.is_read),
        "read_at": _iso(m.read_at) if m.read_at else None, # type: ignore
        "creado_en": _iso(m.created_at) if m.created_at else None, # type: ignore
    }


@router_portal_contacto.get("/mensajes", dependencies=[Depends(varificar_peticion)])
def listar_mensajes(db: Session = Depends(get_db), solo_no_leidos: bool = False):
    q = db.query(CustomerContactMessage).order_by(CustomerContactMessage.id.desc())
    if solo_no_leidos:
        q = q.filter(CustomerContactMessage.is_read.is_(False))
    rows = q.limit(500).all()
    return [_serializar(m) for m in rows]


@router_portal_contacto.get("/mensajes/no-leidos/count", dependencies=[Depends(varificar_peticion)])
def contar_no_leidos(db: Session = Depends(get_db)):
    n = db.query(CustomerContactMessage).filter(CustomerContactMessage.is_read.is_(False)).count()
    return {"count": n}


@router_portal_contacto.patch("/mensajes/{mensaje_id}/leido", dependencies=[Depends(varificar_peticion)])
def marcar_leido(mensaje_id: int, db: Session = Depends(get_db)):
    m = db.query(CustomerContactMessage).filter(CustomerContactMessage.id == mensaje_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado.")
    setattr(m, "is_read", True)
    # Columna sin zona horaria en PostgreSQL (Laravel): guardar naive UTC.
    setattr(m, "read_at", datetime.now(timezone.utc).replace(tzinfo=None))
    commit_or_raise(db)
    db.refresh(m)
    return _serializar(m)


@router_portal_contacto.patch(
    "/mensajes/{mensaje_id}/responder",
    dependencies=[Depends(varificar_peticion)],
)
def responder_mensaje(mensaje_id: int, body: ContactPortalAdminReply, db: Session = Depends(get_db)):
    m = db.query(CustomerContactMessage).filter(CustomerContactMessage.id == mensaje_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado.")
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    setattr(m, "admin_reply", body.admin_reply.strip()[:5000])
    setattr(m, "replied_at", now_naive)
    setattr(m, "is_read", True)
    if m.read_at is None:
        setattr(m, "read_at", now_naive)
    commit_or_raise(db)
    db.refresh(m)
    return _serializar(m)


@router_portal_contacto.delete(
    "/mensajes/{mensaje_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(varificar_peticion)],
)
def eliminar_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    m = db.query(CustomerContactMessage).filter(CustomerContactMessage.id == mensaje_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado.")
    db.delete(m)
    commit_or_raise(db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_portal_contacto.get("/mensajes/por-email", dependencies=[Depends(varificar_peticion)])
def mensajes_por_email(email: str = "", user_id: int = 0, db: Session = Depends(get_db)):
    """Mensajes de un usuario específico (por email y/o user_id)."""
    q = db.query(CustomerContactMessage)
    filters = []
    if email:
        from sqlalchemy import func as sa_func
        filters.append(sa_func.lower(sa_func.trim(CustomerContactMessage.email)) == email.strip().lower())
    if user_id:
        filters.append(CustomerContactMessage.user_id == user_id)
    if not filters:
        return []
    from sqlalchemy import or_
    rows = q.filter(or_(*filters)).order_by(CustomerContactMessage.id.desc()).limit(50).all()
    return [_serializar(m) for m in rows]


@router_portal_contacto.post(
    "/mensajes",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(varificar_peticion)],
)
def crear_mensaje(
    name: str,
    email: str,
    subject: str,
    message: str,
    user_id: int = 0,
    phone: str = "",
    db: Session = Depends(get_db),
):
    """Crea un mensaje de contacto desde el portal Laravel."""
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    m = CustomerContactMessage(
        user_id=user_id if user_id else None,
        name=name,
        email=email.strip().lower(),
        phone=phone if phone else None,
        subject=subject,
        message=message,
        is_read=False,
        created_at=now_naive,
        updated_at=now_naive,
    )
    db.add(m)
    commit_or_raise(db)
    db.refresh(m)
    return _serializar(m)
