<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;

class EstatusPedido extends Model
{
    protected $table = 'estatus_pedido';

    public $timestamps = false;

    protected $fillable = ['nombre', 'modulo', 'color'];
}
