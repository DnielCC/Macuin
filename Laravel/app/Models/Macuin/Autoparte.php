<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasOne;

class Autoparte extends Model
{
    protected $table = 'autopartes';

    public $timestamps = false;

    protected $casts = [
        'precio_unitario' => 'decimal:2',
        'fecha_alta' => 'datetime',
    ];

    protected $fillable = [
        'sku_codigo',
        'nombre',
        'descripcion',
        'precio_unitario',
        'imagen_url',
        'categoria_id',
        'marca_id',
    ];

    public function categoria(): BelongsTo
    {
        return $this->belongsTo(Categoria::class, 'categoria_id');
    }

    public function marca(): BelongsTo
    {
        return $this->belongsTo(Marca::class, 'marca_id');
    }

    public function inventario(): HasOne
    {
        return $this->hasOne(Inventario::class, 'autoparte_id');
    }
}
