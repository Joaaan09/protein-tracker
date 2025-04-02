from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime  # Nuevo: para la fecha/hora
import json

def get_myprotein_price():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get("https://www.myprotein.es/p/nutricion-deportiva/impact-whey-protein/10530943/?variation=10531012")
        
        # Aceptar cookies
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_btn.click()
        except Exception as e:
            print(f"No s'ha pogut acceptar cookies: {e}")
        
        # Extraer precio
        price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-2xl.font-semibold"))
        )
        
        # Limpiar texto
        price_text = price_element.text.split('\n')[-1].replace('€', '').replace(',', '.').strip()
        current_price = float(price_text)
        
        # Generar entrada histórica
        timestamp = datetime.now().isoformat()  # Fecha/hora actual en formato ISO
        
        return {
            "store": "MyProtein",
            "current_price": current_price,
            "discount": 30,
            "price_history": [  # Lista con la entrada actual
                {
                    "price": current_price,
                    "discount": 30,
                    "timestamp": timestamp
                }
            ]
        }
        
    except Exception as e:
        print(f"Error durant el scraping: {e}")
        return {
            "store": "MyProtein",
            "error": str(e)
        }
    
    finally:
        driver.quit()

if __name__ == "__main__":
    result = get_myprotein_price()
    print(json.dumps(result, ensure_ascii=False))  # Asegura caracteres especiales