from fastapi import FastAPI
import requests
import uvicorn

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
    except Exception:
        return False

@app.get("/")
def root():
    return {"status": "running", "message": "Flipkart Availability Checker API"}

@app.get("/check")
def check(url: str, pincodes: str):
    product_id = extract_product_id(url)
    if not product_id:
        return {"error": "Invalid Flipkart URL"}

    pins = pincodes.split(",")
    results = {}
    for pin in pins:
        results[pin.strip()] = check_availability(product_id, pin.strip())
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
