<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class DetallePedido extends Model
{
    protected $table = 'detalles_pedidos';

    public $timestamps = false;

    protected $casts = [
        'cantidad' => 'integer',
        'precio_historico' => 'decimal:2',
    ];

    protected $fillable = [
        'pedido_id',
        'autoparte_id',
        'cantidad',
        'precio_historico',
    ];

    public function pedido(): BelongsTo
    {
        return $this->belongsTo(Pedido::class, 'pedido_id');
    }

    public function autoparte(): BelongsTo
    {
        return $this->belongsTo(Autoparte::class, 'autoparte_id');
    }
}
