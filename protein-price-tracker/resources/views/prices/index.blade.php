<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparador de Preus de Proteïna</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-6">Comparador de Preus de Proteïna</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            @foreach($prices as $price)
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <div class="flex justify-between items-start">
                        <div>
                            <h2 class="text-xl font-semibold">{{ $price->store }}</h2>
                            <p class="text-gray-700 mt-2">Preu actual: <span class="font-bold">{{ number_format($price->price, 2) }}€</span></p>
                            <p class="text-gray-700">Descompte: <span class="font-bold">{{ $price->discount }}%</span></p>
                        </div>
                        <span class="text-sm text-gray-500">{{ $price->updated_at->diffForHumans() }}</span>
                    </div>
                    
                    @if(!empty($price->price_history))
                        <div class="mt-6">
                            <h3 class="text-lg font-medium mb-2">Evolució del preu</h3>
                            <div class="h-64">
                                <canvas id="chart-{{ $price->id }}"></canvas>
                            </div>
                        </div>
                        
                        <script>
                            document.addEventListener('DOMContentLoaded', function() {
                                const history = @json($price->price_history);
                                const ctx = document.getElementById('chart-{{ $price->id }}').getContext('2d');
                                
                                new Chart(ctx, {
                                    type: 'line',
                                    data: {
                                        labels: history.map(entry => new Date(entry.timestamp).toLocaleDateString()),
                                        datasets: [{
                                            label: 'Preu (€)',
                                            data: history.map(entry => entry.price),
                                            borderColor: 'rgb(59, 130, 246)',
                                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                            tension: 0.1,
                                            fill: true
                                        }]
                                    },
                                    options: {
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        scales: {
                                            y: {
                                                beginAtZero: false,
                                                title: {
                                                    display: true,
                                                    text: 'Preu (€)'
                                                }
                                            },
                                            x: {
                                                title: {
                                                    display: true,
                                                    text: 'Data'
                                                }
                                            }
                                        }
                                    }
                                });
                            });
                        </script>
                    @else
                        <p class="text-gray-500 mt-4">No hi ha dades històriques disponibles</p>
                    @endif
                </div>
            @endforeach
        </div>
    </div>
</body>
</html>