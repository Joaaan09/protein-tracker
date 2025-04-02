<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Price; // Importa el model Price

class PricesTableSeeder extends Seeder
{
    public function run()
    {
        // Neteja la taula abans d'afegir dades (opcional)
        Price::truncate();

        // Afegeix dades d'exemple
        Price::create([
            'store' => 'MyProtein',
            'price' => 24.99,
            'discount' => 30,
        ]);

        Price::create([
            'store' => 'Prozis',
            'price' => 22.50,
            'discount' => 25,
        ]);

        Price::create([
            'store' => 'Amazon',
            'price' => 26.75,
            'discount' => 15,
        ]);
    }
}