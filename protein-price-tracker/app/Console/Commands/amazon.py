def get_amazon_price():
    # Ús de l'API de RapidAPI per evitar problemes amb scraping directe
    import requests
    
    url = "https://amazon-price2.p.rapidapi.com/price"
    querystring = {"asin":"B07ZPLM8R7","marketplace":"ES"}
    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY",
        "X-RapidAPI-Host": "amazon-price2.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    return {
        "store": "Amazon",
        "price": float(data['price']),
        "discount": data.get('discount_percent', 0)
    }