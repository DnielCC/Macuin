<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Carrito extends Model
{
    protected $table = 'carritos';

    public $timestamps = false;

    protected $casts = [
        'creado_en' => 'datetime',
        'actualizado_en' => 'datetime',
    ];

    protected $fillable = [
        'uuid',
        'laravel_user_id',
        'email_invitado',
    ];

    public function lineas(): HasMany
    {
        return $this->hasMany(CarritoLinea::class, 'carrito_id');
    }
}
