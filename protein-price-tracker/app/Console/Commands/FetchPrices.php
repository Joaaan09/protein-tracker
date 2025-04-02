<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Price;
use Illuminate\Support\Carbon;

class FetchPrices extends Command
{
    protected $signature = 'prices:fetch';
    protected $description = 'Fetch prices from MyProtein and Prozis and store with price history';

    public function handle()
    {
        $command = escapeshellcmd('python3 ' . base_path('app/Console/Commands/run_scrappers.py'));
        $output = shell_exec($command);
        
        $this->line("Raw Python output:");
        $this->line($output);
        
        $data = json_decode($output, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            $this->error("Error decoding JSON: " . json_last_error_msg());
            return 1;
        }
        
        foreach ($data as $scraperName => $result) {
            $this->newLine();
            $this->info("Processing {$scraperName}...");
            
            if (isset($result['error'])) {
                $this->error("Error in {$scraperName}: {$result['error']}");
                continue;
            }
            
            try {
                // Obtener o crear el registro
                $priceRecord = Price::firstOrNew(['store' => $result['store']]);
                
                // Convertir price_history a array si es string
                $existingHistory = [];
                if (!empty($priceRecord->price_history)) {
                    $existingHistory = is_string($priceRecord->price_history)
                        ? json_decode($priceRecord->price_history, true)
                        : $priceRecord->price_history;
                }
                
                // Añadir nueva entrada al histórico
                $newHistoryEntry = [
                    'price' => $result['current_price'],
                    'discount' => $result['discount'],
                    'timestamp' => Carbon::now()->toISOString()
                ];
                
                $existingHistory[] = $newHistoryEntry;
                
                // Limitar histórico (últimos 30 registros)
                $maxHistoryEntries = 30;
                if (count($existingHistory) > $maxHistoryEntries) {
                    $existingHistory = array_slice($existingHistory, -$maxHistoryEntries);
                }
                
                // Actualizar registro
                $priceRecord->price = $result['current_price'];
                $priceRecord->discount = $result['discount'];
                $priceRecord->price_history = $existingHistory;
                $priceRecord->save();
                
                $this->info("✅ {$result['store']} updated!");
                
            } catch (\Exception $e) {
                $this->error("Error saving {$result['store']}: " . $e->getMessage());
            }
        }
        
        $this->newLine();
        $this->info("🏁 Price update completed!");
        return 0;
    }
}