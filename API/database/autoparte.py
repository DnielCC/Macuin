from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

class Autoparte(Base):
    __tablename__ = "autopartes"

    id = Column(Integer, primary_key=True, index=True)
    sku_codigo = Column(String(50), nullable=False, unique=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    marca_id = Column(Integer, ForeignKey("marcas.id"), nullable=False)
    fecha_alta = Column(DateTime(timezone=True), server_default=func.now())
    esta_activo = Column(Boolean, default=True)

    categoria = relationship("Categoria", backref="autopartes")
    marca = relationship("Marca", backref="autopartes")

    # Relaciones para borrado lógico (Soft Delete)
    # Al "borrar", desactivamos la autoparte y borramos su inventario/carritos físicamente
    inventario_rec = relationship("Inventario", back_populates="autoparte", cascade="all, delete-orphan", uselist=False)
    items_carrito = relationship("CarritoLinea", back_populates="autoparte", cascade="all, delete-orphan")
    detalles_pedidos = relationship("DetallePedido", back_populates="autoparte")