<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Pago extends Model
{
    protected $table = 'pagos';

    public $timestamps = false;

    protected $casts = [
        'monto' => 'decimal:2',
        'creado_en' => 'datetime',
    ];

    protected $fillable = [
        'pedido_id',
        'carrito_id',
        'monto',
        'moneda',
        'estado',
        'pasarela',
        'referencia_externa',
        'respuesta_proveedor',
    ];

    public function pedido(): BelongsTo
    {
        return $this->belongsTo(Pedido::class, 'pedido_id');
    }
}
