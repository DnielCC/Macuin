<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Usuario interno (tabla usuarios) para pedidos creados desde el portal
    |--------------------------------------------------------------------------
    |
    | Los pedidos en PostgreSQL requieren usuario_id (empleado interno).
    | Se usa un usuario real existente (por defecto el de ventas del seed).
    |
    */
    'portal_usuario_email' => env('MACUIN_PORTAL_USUARIO_EMAIL', 'ventas@macuin.com'),

    /*
    |--------------------------------------------------------------------------
    | Costo de envío fijo (simulación checkout)
    |--------------------------------------------------------------------------
    */
    'envio_fijo_mxn' => (float) env('MACUIN_ENVIO_FIJO_MXN', 150),

    /*
    |--------------------------------------------------------------------------
    | Pasarela simulada
    |--------------------------------------------------------------------------
    */
    'pasarela_nombre' => env('MACUIN_PASARELA_NOMBRE', 'Simulación MACUIN'),

    /*
    |--------------------------------------------------------------------------
    | Correos que pueden ver la bandeja de contacto en Laravel
    |--------------------------------------------------------------------------
    |
    | Lista separada por comas. Si está vacía, cualquier usuario autenticado
    | cuyo email esté en ADMIN_CONTACT_EMAILS (también CSV) puede acceder.
    |
    */
    'admin_contact_emails' => array_values(array_filter(array_map(
        'trim',
        explode(',', (string) env('MACUIN_ADMIN_CONTACT_EMAILS', 'admin@macuin.com'))
    ))),

    /*
    |--------------------------------------------------------------------------
    | API FastAPI (sincronizar mensajes de contacto → panel Flask)
    |--------------------------------------------------------------------------
    */
    'api_base_url' => rtrim((string) env('API_BASE_URL', 'http://localhost:8000'), '/'),

    'api_basic_user' => (string) env('API_BASIC_USER', 'alidaniel'),
    
    'api_basic_password' => (string) env('API_BASIC_PASSWORD', '123456'),

    /** Token compartido con PORTAL_CONTACTO_SYNC_TOKEN en el servicio API. */
    'portal_contact_sync_token' => (string) env('MACUIN_PORTAL_CONTACT_SYNC_TOKEN', ''),

];
