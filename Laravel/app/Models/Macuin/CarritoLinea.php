<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class CarritoLinea extends Model
{
    protected $table = 'carrito_lineas';

    public $timestamps = false;

    protected $casts = [
        'cantidad' => 'integer',
        'precio_unitario' => 'decimal:2',
    ];

    protected $fillable = [
        'carrito_id',
        'autoparte_id',
        'cantidad',
        'precio_unitario',
    ];

    public function carrito(): BelongsTo
    {
        return $this->belongsTo(Carrito::class, 'carrito_id');
    }

    public function autoparte(): BelongsTo
    {
        return $this->belongsTo(Autoparte::class, 'autoparte_id');
    }
}
