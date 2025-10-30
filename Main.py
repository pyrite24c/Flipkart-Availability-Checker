from fastapi import FastAPI
import requests

app = FastAPI()

def extract_product_id(url: str):
    parts = url.split("/p/")
    if len(parts) < 2:
        return None
    return parts[1].split("/")[0]

def check_availability(product_id, pincode):
    try:
        url = f"https://www.flipkart.com/api/3/product/{product_id}?pincode={pincode}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        res = requests.get(url, headers=headers, timeout=10)
        data = res.text.lower()
        if "deliverable" in data or "deliverymessage" in data:
            return True
        return False
    except:
        return False

@app.get("/check")
def check(url: str, pincodes: str):
    product_id = extract_product_id(url)
    if not product_id:
        return {"error": "invalid url"}

    pins = pincodes.split(",")
    results = {}
    for pin in pins:
        results[pin] = check_availability(product_id, pin.strip())
    return results
