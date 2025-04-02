<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
// database/migrations/xxxx_xx_xx_create_prices_table.php
public function up()
{
    Schema::create('prices', function (Blueprint $table) {
        $table->id();
        $table->string('store'); // MyProtein, Prozis, Amazon
        $table->decimal('price', 8, 2); // Preu actual
        $table->decimal('discount', 5, 2); // Descompte
        $table->timestamps(); // created_at i updated_at
    });
}

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('prices');
    }
};
