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
        "id": int(m.id),
        "laravel_contact_message_id": int(m.id),
        "nombre": m.name,
        "email": m.email,
        "telefono": m.phone,
        "asunto": m.subject,
        "mensaje": m.message,
        "admin_reply": m.admin_reply,
        "replied_at": _iso(m.replied_at) if m.replied_at else None,
        "is_read": bool(m.is_read),
        "read_at": _iso(m.read_at) if m.read_at else None,
        "creado_en": _iso(m.created_at) if m.created_at else None,
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
    m.is_read = True
    # Columna sin zona horaria en PostgreSQL (Laravel): guardar naive UTC.
    m.read_at = datetime.now(timezone.utc).replace(tzinfo=None)
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
    m.admin_reply = body.admin_reply.strip()[:5000]
    m.replied_at = now_naive
    m.is_read = True
    if m.read_at is None:
        m.read_at = now_naive
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
