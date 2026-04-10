from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base


class Carrito(Base):
    """Carrito de compras (portal Laravel u otros clientes; sin FK a users para no depender del orden de migraciones)."""

    __tablename__ = "carritos"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False, index=True)
    laravel_user_id = Column(Integer, nullable=True, index=True)
    email_invitado = Column(String(120), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    lineas = relationship("CarritoLinea", back_populates="carrito", cascade="all, delete-orphan")


class CarritoLinea(Base):
    __tablename__ = "carrito_lineas"

    id = Column(Integer, primary_key=True, index=True)
    carrito_id = Column(Integer, ForeignKey("carritos.id", ondelete="CASCADE"), nullable=False, index=True)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)

    carrito = relationship("Carrito", back_populates="lineas")
    autoparte = relationship("Autoparte", backref="lineas_carrito")
