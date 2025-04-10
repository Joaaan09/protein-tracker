<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up()
    {
        Schema::create('prices', function (Blueprint $table) {
            $table->id();
            $table->string('store'); // MyProtein, Prozis, Amazon
            $table->decimal('price', 8, 2); // Preu actual
            $table->decimal('discount', 5, 2); // Descompte
            $table->string('codigo')->nullable(); // Nou camp: codi identificador
            $table->json('price_history')->nullable(); // Nou camp: historial de preus
	    $table->string('url')->nullable(); //Url del producte
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

