<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Inventario extends Model
{
    protected $table = 'inventarios';

    public $timestamps = false;

    protected $casts = [
        'stock_actual' => 'integer',
        'stock_minimo' => 'integer',
    ];

    protected $fillable = [
        'autoparte_id',
        'ubicacion_id',
        'stock_actual',
        'stock_minimo',
        'pasillo',
        'estante',
        'nivel',
    ];

    public function autoparte(): BelongsTo
    {
        return $this->belongsTo(Autoparte::class, 'autoparte_id');
    }
}
