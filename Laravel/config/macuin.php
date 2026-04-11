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

];
