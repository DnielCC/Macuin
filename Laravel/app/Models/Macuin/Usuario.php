<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;

class Usuario extends Model
{
    protected $table = 'usuarios';

    public $timestamps = false;

    protected $hidden = ['password_hash'];

    protected $casts = [
        'activo' => 'boolean',
    ];
}
