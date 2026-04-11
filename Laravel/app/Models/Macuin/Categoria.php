<?php

namespace App\Models\Macuin;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Categoria extends Model
{
    protected $table = 'categorias';

    public $timestamps = false;

    protected $fillable = ['nombre'];

    public function autopartes(): HasMany
    {
        return $this->hasMany(Autoparte::class, 'categoria_id');
    }
}
