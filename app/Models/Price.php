<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;


class Price extends Model
{
    use HasFactory;

    protected $fillable = ['store', 'price', 'discount', "price_history", 'codigo']; // Camps que es poden assignar massivament
    protected $casts = [
        'price_history' => 'array' // Esto convierte automáticamente el JSON a array
    ];
}
