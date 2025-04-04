from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime  # Para el timestamp
import json
import tempfile
import os
import sys

def get_myprotein_price():
    # Crear un directorio temporal para el perfil de Chrome
    user_data_dir = tempfile.mkdtemp()

    # Configurar las opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Directorio único
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless, opcional

    # Inicializar el driver con webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Abrir la página del producto
        driver.get("https://www.myprotein.es/p/nutricion-deportiva/impact-whey-protein/10530943/?variation=10531012")

        # Aceptar cookies
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_btn.click()
        except Exception as e:
            print(f"No se pudieron aceptar las cookies: {e}")

        # Esperar y hacer clic en el botón "Añadir a la cesta"
        add_to_basket_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "add-to-basket"))
        )
        add_to_basket_btn.click()

        # Esperar a que aparezca el pop-up y seleccionar "Ver la cesta"
        view_basket_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "view-basket-btn"))
        )
        view_basket_btn.click()

        # Ahora estamos en la página de la cesta.
        # Extraer el precio: se busca el <span> con clase "font-bold text-lg" dentro del div con clase "item-price space-y-2 text-left"
        price_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.item-price.space-y-2.text-left span.font-bold.text-lg")
            )
        )
        price_text = price_element.text.replace('€', '').replace(',', '.').strip()
        current_price = float(price_text)

        # Buscar el input para el código promo y enviar el código "andoni"
        promo_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "promo-code-input"))
        )
        promo_input.clear()
        promo_input.send_keys("andoni")

        # Hacer clic en el botón para agregar el código promocional
        promo_add_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "promo-code-add"))
        )
        promo_add_btn.click()

        # Esperar a que aparezca el porcentaje de descuento en el <span> con clase "ml-1" dentro de un <p> con clase "bg-accent"
        discount_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.bg-accent span.ml-1"))
        )
        discount_text = discount_element.text.replace('%', '').replace('(', '').replace(')', '').strip()
        discount = float(discount_text)

        # Generar la entrada histórica con timestamp actual
        timestamp = datetime.now().isoformat()

        return {
            "store": "MyProtein",
            "current_price": current_price,
            "discount": discount,
	    "codigo": "andoni",
            "price_history": [{
                "price": current_price,
                "discount": discount,
                "timestamp": timestamp,
		"codigo": "andoni"
            }]
        }
    except Exception as e:
        print(f"Error en myprotein: {e}", file=sys.stderr)
        return {"error": str(e)}
    finally:
        driver.quit()

if __name__ == "__main__":
    try:
        data = get_myprotein_price()
        print(json.dumps(data, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

