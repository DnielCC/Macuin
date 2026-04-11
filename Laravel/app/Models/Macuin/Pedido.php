<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Pedido extends Model
{
    protected $table = 'pedidos';

    public $timestamps = false;

    protected $casts = [
        'total' => 'decimal:2',
        'fecha_pedido' => 'datetime',
        'fecha_cancelacion' => 'datetime',
    ];

    protected $fillable = [
        'folio',
        'usuario_id',
        'estatus_id',
        'total',
        'direccion_envio_id',
        'cliente_id',
        'motivo_cancelacion',
        'fecha_cancelacion',
    ];

    public function cliente(): BelongsTo
    {
        return $this->belongsTo(Cliente::class, 'cliente_id');
    }

    public function estatus(): BelongsTo
    {
        return $this->belongsTo(EstatusPedido::class, 'estatus_id');
    }

    public function detalles(): HasMany
    {
        return $this->hasMany(DetallePedido::class, 'pedido_id');
    }
}
