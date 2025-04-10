from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime  # Nuevo: para el timestamp
import json
from selenium.webdriver.chrome.options import Options

def get_prozis_price():
    # Configuración de las opciones del navegador
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar sin cabeza (sin interfaz gráfica)
    chrome_options.add_argument("--disable-gpu")  # Desactivar la GPU para evitar errores en algunos entornos
    chrome_options.add_argument("--window-size=1920x1080")  # Simular resolución de pantalla
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Usar webdriver-manager para instalar y manejar ChromeDriver automáticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.prozis.com/es/es/prozis/100-real-whey-protein-1000-g")
        
        # Aceptar cookies
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_btn.click()
        except Exception as e:
            print(f"No s'ha pogut acceptar cookies: {e}")
        
        # Extraer precio
        price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.final-price"))
        )
        
        # Procesar precio
        price_text = price_element.get_attribute("data-qa").replace('€', '').strip()
        current_price = float(price_text)
        
        # Generar entrada histórica
        timestamp = datetime.now().isoformat()  # Fecha/hora en formato ISO
        
        return {
            "store": "Prozis",
            "current_price": current_price,  # Cambiado de "price" a "current_price"
            "discount": 10,
	    "codigo": "juan",
	    "url": "https://www.prozis.com/es/es/prozis/100-real-whey-protein-1000-g",
            "price_history": [  # Nuevo campo para el histórico
                {
                    "price": current_price,
                    "discount": 10,
                    "timestamp": timestamp,
		    "codigo": "juan"
                }
            ]
        }
    
    except Exception as e:
        print(f"Error durant el scraping: {e}")
        return {
            "store": "Prozis",
            "error": str(e)
        }
    
    finally:
        driver.quit()

if __name__ == "__main__":
    result = get_prozis_price()
    print(json.dumps(result, ensure_ascii=False))  # Añadido ensure_ascii para caracteres especiales
