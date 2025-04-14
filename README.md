# Comparador de Precios de Proteínas  

Sistema Laravel + Python que monitorea precios de suplementos proteicos en MyProtein y otras tiendas, con historial de precios y alertas.
En el caso de MyProtein, se accede al enlace de la proteína sin sabor de 1 kg, se añade al carrito, se aplica el código de descuento y finalmente se obtiene el precio original (sin descuento), el porcentaje de descuento y se calcula el precio final.

En Prozis, se accede a la proteína sin sabor de 1 kg y se obtiene el precio. El descuento se ha calculado manualmente: he ingresado el código de descuento de manera manual y comprobado el porcentaje de descuento, ya que, si intentara hacer el proceso igual que en MyProtein, se requiere iniciar sesión, lo que el scrapper no puede hacer tal como está diseñado.

En el caso de Amazon, realicé una búsqueda de "proteína whey 1 kg sin sabor" y ordené los resultados de menor a mayor precio. El scrapper se encarga de obtener el primer producto, que es el más barato, y extrae su precio. En este caso, no hay descuento aplicado.
## Características principales  

- ✅ Scraping automatizado con Selenium (Python)  
- ✅ Base de datos SQLite integrada  
- ✅ Historial completo de precios  
- ✅ Fácil expansión a nuevas tiendas  
- ✅ Comando CLI integrado (`php artisan prices:fetch`)  

## Requisitos  

- **PHP >= 8.1**  
- **Composer**  
- **Laravel 10+**  
- **SQLite** (no requiere servidor de base de datos)  
- **Python 3.10+** con pip  
- **Google Chrome** (última versión estable)  
- **ChromeDriver** (se instala automáticamente)  

## Instalación rápida  

1. Clona el repositorio:  
```bash  
git clone https://github.com/Joaaan09/protein-tracker  
cd protein-price-tracker  
```  

2. Instala dependencias PHP:  
```bash  
composer install  
```  

3. Configura el entorno:  
```bash  
cp .env.example .env  
```  

4. Configura SQLite en el `.env`:  
```bash  
echo "DB_CONNECTION=sqlite" >> .env  
echo "DB_DATABASE=${PWD}/database/database.sqlite" >> .env  
```  

5. Crea la base de datos:  
```bash  
touch database/database.sqlite  
```  

6. Genera la clave de Laravel:  
```bash  
php artisan key:generate  
```  

7. Ejecuta las migraciones:  
```bash  
php artisan migrate  
```  

8. Instala dependencias Python:  
```bash  
pip install selenium webdriver-manager  
```  

## Uso básico  

Actualizar precios:  
```bash  
php artisan prices:fetch  
```  

Iniciar servidor web local:  
```bash  
php artisan serve  
```  

## Para desarrolladores  

### Estructura de scrapers Python  
Los scrapers se encuentran en `/app/Console/Commands`:  
- `myprotein.py` - Scraper principal para MyProtein  
- `prozis.py` - Scraper principal para Prozis
- `amazon.py` - Scraper principal para Amazon
- `run_scrappers.py` - Programa que ejecuta los scrappers 

### Testear scrapers individualmente  
```bash  
python3 scrapers/myprotein.py
```  

### Variables de entorno importantes  
```dotenv  
SCRAPER_HEADLESS=true  # Ejecución sin interfaz gráfica  
SCRAPER_TIMEOUT=30     # Timeout en segundos  
```  

### Cómo añadir una nueva tienda  
1. Crea un nuevo archivo `nuevatienda_scraper.py` en `/app/Console/Commands`  
2. Implementa la función `get_prices()`  
3. Registra el scraper en `app/Console/Commands/run_scrappers.php`  

## Solución de problemas  

**Error:** ChromeDriver no se inicia  
- Verifica que tienes Google Chrome instalado  
- Ejecuta `google-chrome --version` y asegúrate que coincide con la versión de ChromeDriver  


## Licencia  

MIT License - Libre uso y modificación
