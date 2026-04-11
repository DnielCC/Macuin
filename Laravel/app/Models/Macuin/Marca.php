<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Marca extends Model
{
    protected $table = 'marcas';

    public $timestamps = false;

    protected $fillable = ['nombre'];

    public function autopartes(): HasMany
    {
        return $this->hasMany(Autoparte::class, 'marca_id');
    }
}
