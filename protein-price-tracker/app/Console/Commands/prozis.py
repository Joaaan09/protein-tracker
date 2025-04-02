from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime  # Nuevo: para el timestamp
import json

def get_prozis_price():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get("https://www.prozis.com/es/es/prozis/100-real-whey-protein-1000-g")
        
        # Acceptar cookies
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
            "discount": 25,
            "price_history": [  # Nuevo campo para el histórico
                {
                    "price": current_price,
                    "discount": 25,
                    "timestamp": timestamp
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