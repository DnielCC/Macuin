"""Mensajes del formulario de contacto del portal Laravel (tabla compartida en PostgreSQL)."""

from sqlalchemy import BigInteger, Boolean, Column, DateTime, String, Text

from database.db import Base


class CustomerContactMessage(Base):
    """
    Misma tabla que crea Laravel (`contact_messages`).
    La API solo lee/actualiza para el panel Flask; el alta lo hace Laravel.
    """

    __tablename__ = "contact_messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=True)
    name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(40), nullable=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    admin_reply = Column(Text, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
