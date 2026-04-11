<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Direccion extends Model
{
    protected $table = 'direcciones';

    public $timestamps = false;

    protected $fillable = [
        'calle_principal',
        'num_ext',
        'num_int',
        'colonia',
        'municipio',
        'estado',
        'cp',
        'referencias',
        'cliente_id',
    ];

    public function cliente(): BelongsTo
    {
        return $this->belongsTo(Cliente::class, 'cliente_id');
    }
}
