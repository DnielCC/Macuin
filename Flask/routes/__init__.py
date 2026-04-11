def register_routes(app):
    from . import (
        admin_segment,
        almacen_segment,
        auth_segment,
        core_segment,
        logistica_segment,
        reportes_segment,
        ventas_segment,
    )

    auth_segment.register(app)
    core_segment.register(app)
    admin_segment.register(app)
    ventas_segment.register(app)
    logistica_segment.register(app)
    almacen_segment.register(app)
    reportes_segment.register(app)
