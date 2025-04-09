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
    chrome_options.add_argument("--headless")  # Quitar si quieres ver lo que hace
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=es-ES")  # Idioma español

    # Inicializar el driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://www.amazon.es/s?k=proteina+whey+1kg+sin+sabor&s=price-asc-rank&ds=v1%3ArnTSm%2FJl3JTrK6cGp48IzLHogBrKg0meaW2VufxPhj0&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1J0M7L335C4VP&qid=1743701106&sprefix=proteina+whey+1kg+sin+sabor%2Caps%2C96&ref=sr_st_price-asc-rank"
        driver.get(url)

        # Aceptar cookies si es necesario
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
            )
            cookie_btn.click()
        except:
            pass  # Si no aparece el banner, seguimos

        # Esperar a que se cargue el primer producto
        first_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
        )

        # Extraer precio (puede estar dividido en euros y céntimos)
        try:
            whole_price = first_product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.replace(".", "").strip()
            fraction_price = first_product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text.strip()
            price_text = f"{whole_price}.{fraction_price}"
            price = float(price_text)
        except Exception as e:
            raise Exception("No se pudo extraer el precio del primer producto")

        # Timestamp actual
        timestamp = datetime.now().isoformat()

        return {
            "store": "Amazon",
            "current_price": price,
            "discount": 0,
            "codigo": "Sense codi",
            "price_history": [{
                "price": price,
                "timestamp": timestamp,
                "codigo": "Sense codi",
                "discount": 0
            }]
        }

    except Exception as e:
        print(f"Error en Amazon: {e}", file=sys.stderr)
        return {"error": str(e)}
    finally:
        driver.quit()

if __name__ == "__main__":
    try:
        data = get_amazon_price()
        print(json.dumps(data, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
