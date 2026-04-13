"""Endpoint transaccional de checkout para el portal Laravel.

Recibe todo el payload (cliente, dirección, líneas, pago) y ejecuta la operación
completa dentro de una sola transacción SQL.  Así Laravel no necesita acceso directo
a la base de datos.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.carrito import Carrito, CarritoLinea
from database.cliente import Cliente
from database.db import get_db
from database.detalle_pedido import DetallePedido
from database.direccion import Direccion
from database.estatus_pedido import EstatusPedido
from database.pago import Pago
from database.pedido import Pedido
from database.usuario import Usuario
from models.portal_checkout import PortalCheckoutRequest
from security.auth import varificar_peticion

router_portal_checkout = APIRouter(
    prefix="/v1/portal",
    tags=["Portal Laravel"],
    dependencies=[Depends(varificar_peticion)],
)


@router_portal_checkout.post("/checkout", status_code=201)
def portal_checkout(body: PortalCheckoutRequest, db: Session = Depends(get_db)):
    """Procesa un pedido completo de forma transaccional (cliente, dirección, pedido, detalles, pago)."""

    # 1. Resolver usuario interno
    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == body.usuario_email.strip().lower())
        .first()
    )
    if not usuario:
        raise HTTPException(
            status_code=400,
            detail=f"No existe el usuario interno con email «{body.usuario_email}».",
        )

    # 2. Estatus "Pendiente"
    estatus = db.query(EstatusPedido).filter(EstatusPedido.nombre == "Pendiente").first()
    if not estatus:
        raise HTTPException(
            status_code=500,
            detail="No existe el estatus «Pendiente» en la base de datos. Ejecuta el seed.",
        )

    try:
        # 3. Cliente (first or create by email)
        email_lower = body.cliente.email.strip().lower()
        cliente = db.query(Cliente).filter(Cliente.email == email_lower).first()
        if not cliente:
            cliente = Cliente(
                nombre=body.cliente.nombre,
                email=email_lower,
                telefono=body.cliente.telefono,
                activo=True,
                notas="Portal Laravel — checkout API",
            )
            db.add(cliente)
            db.flush()

        # 4. Dirección
        direccion = Direccion(
            calle_principal=body.direccion.calle_principal,
            num_ext=body.direccion.num_ext,
            num_int=body.direccion.num_int,
            colonia=body.direccion.colonia,
            municipio=body.direccion.municipio,
            estado=body.direccion.estado,
            cp=body.direccion.cp,
            referencias=body.direccion.referencias,
            cliente_id=cliente.id,
        )
        db.add(direccion)
        db.flush()

        # 5. Pedido
        total = body.pago.monto
        pedido = Pedido(
            folio=body.folio,
            usuario_id=usuario.id,
            estatus_id=estatus.id,
            total=total,
            direccion_envio_id=direccion.id,
            cliente_id=cliente.id,
        )
        db.add(pedido)
        db.flush()

        # 6. Detalles
        for ln in body.lineas:
            detalle = DetallePedido(
                pedido_id=pedido.id,
                autoparte_id=ln.autoparte_id,
                cantidad=ln.cantidad,
                precio_historico=ln.precio_unitario,
            )
            db.add(detalle)

        # 7. Pago
        pago = Pago(
            pedido_id=pedido.id,
            carrito_id=None,
            monto=body.pago.monto,
            moneda=body.pago.moneda,
            estado=body.pago.estado,
            pasarela=body.pago.pasarela,
            referencia_externa=body.pago.referencia_externa,
            respuesta_proveedor=body.pago.respuesta_proveedor,
        )
        db.add(pago)

        # 8. Limpiar carrito si se proporcionó
        if body.carrito_id:
            db.query(CarritoLinea).filter(
                CarritoLinea.carrito_id == body.carrito_id
            ).delete(synchronize_session=False)
            db.query(Carrito).filter(Carrito.id == body.carrito_id).delete(
                synchronize_session=False
            )

        db.commit()
        db.refresh(pedido)
        db.refresh(pago)

        return {
            "ok": True,
            "message": "Pedido registrado correctamente.",
            "pedido_id": pedido.id,
            "pago_id": pago.id,
            "folio": pedido.folio,
        }

    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar checkout: {exc!s}",
        ) from exc
