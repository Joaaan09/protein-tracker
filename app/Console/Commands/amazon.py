from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import tempfile
import json
import sys

def get_amazon_price():
    # Crear un perfil temporal para evitar problemas de caché y cookies
    user_data_dir = tempfile.mkdtemp()

    # Opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=es-ES")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        urlSearch = "https://www.amazon.es/s?k=proteina+whey+1kg+sin+sabor&s=price-asc-rank&ds=v1%3ArnTSm%2FJl3JTrK6cGp48IzLHogBrKg0meaW2VufxPhj0"
        driver.get(urlSearch)

        # Aceptar cookies si aparece
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
            )
            cookie_btn.click()
        except:
            pass

        # Esperar a que se cargue el primer producto
        first_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
        )

        # Precio
        try:
            whole_price = first_product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.replace(".", "").strip()
            fraction_price = first_product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text.strip()
            price_text = f"{whole_price}.{fraction_price}"
            price = float(price_text)
        except Exception as e:
            raise Exception("No se pudo extraer el precio del primer producto")

        # URL del producto
        try:
            link_element = first_product.find_element(By.CSS_SELECTOR, "a.a-link-normal")
            url = link_element.get_attribute("href")
        except Exception as e:
            url = None  # Si no se puede extraer la URL, dejamos que sea None

        # Timestamp actual
        timestamp = datetime.now().isoformat()

        # Devolver el JSON con los datos obtenidos
        result = {
            "store": "Amazon",
            "current_price": price,
            "discount": 0,
            "codigo": "Sense codi",
            "url": url if url else "No URL available",  # Añadir mensaje si no tiene URL
            "price_history": [{
                "price": price,
                "timestamp": timestamp,
                "codigo": "Sense codi",
                "discount": 0
            }]
        }

        # Imprimir el resultado para asegurarnos de que se muestra algo
        print(json.dumps(result, ensure_ascii=False))

        return result

    except Exception as e:
        # Capturar el error y devolverlo en formato JSON
        error_result = {"error": f"Error en Amazon: {str(e)}"}
        print(json.dumps(error_result, ensure_ascii=False))
        return error_result

    finally:
        driver.quit()

if __name__ == "__main__":
    get_amazon_price()
