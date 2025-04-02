<?php

namespace App\Http\Controllers;

use App\Models\Price;
use Illuminate\Http\Request;

class PriceController extends Controller
{
    public function index()
    {
        // Obtener precios ordenados y asegurar que el histórico es un array
        $prices = Price::orderBy('created_at', 'desc')
                    ->get()
                    ->each(function ($price) {
                        // Convertir price_history a array si es necesario
                        if (is_string($price->price_history)) {
                            $price->price_history = json_decode($price->price_history, true);
                        }
                        return $price;
                    });
        
        return view('prices.index', [
            'prices' => $prices,
            'stores' => $prices->pluck('store')->unique() // Para posibles filtros futuros
        ]);
    }
}