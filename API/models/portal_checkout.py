"""Pydantic models for the portal checkout endpoint."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class CheckoutLineaItem(BaseModel):
    autoparte_id: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., ge=0)


class CheckoutDireccion(BaseModel):
    calle_principal: str
    num_ext: str
    num_int: Optional[str] = None
    colonia: str
    municipio: str
    estado: str
    cp: str
    referencias: Optional[str] = None


class CheckoutCliente(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None


class CheckoutPago(BaseModel):
    monto: float
    moneda: str = "MXN"
    estado: str = "aprobado"
    pasarela: Optional[str] = None
    referencia_externa: Optional[str] = None
    respuesta_proveedor: Optional[str] = None


class PortalCheckoutRequest(BaseModel):
    """All-in-one checkout payload sent by Laravel portal."""

    folio: str
    usuario_email: str  # email of internal user (e.g. ventas@macuin.com)
    cliente: CheckoutCliente
    direccion: CheckoutDireccion
    lineas: list[CheckoutLineaItem] = Field(..., min_length=1)
    pago: CheckoutPago
    carrito_id: Optional[int] = None  # carrito to clean up after order
