#DB ficticia
usuarios_db = [
    {"id": 1, "nombre": "Juan Perez", "email": "juan@macuin.com", "rol": "ADMIN"},
    {"id": 2, "nombre": "Maria Lopez", "email": "maria@cliente.com", "rol": "CLIENTE"}
]

autopartes_db = [
    {"id": 1, "sku": "BTO-001", "nombre": "Bomba de Agua", "precio": 450.50, "stock": 10},
    {"id": 2, "sku": "FRN-002", "nombre": "Balatas Delanteras", "precio": 890.00, "stock": 5}
]

pedidos_db = [
    {"id": 1, "usuario_id": 2, "total": 890.00, "estatus": "PENDIENTE"}
]