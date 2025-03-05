from fastapi import FastAPI, HTTPException
import requests
app = FastAPI()
# API Key and Google Sheet ID
API_KEY = "AIzaSyDOs-Wl2bTLvL5jyipmsh1yZgnLTJUlXdE"
SHEET_ID = "1pNElAU53yw3Db-Gjhg8nWaaWejL7XNHMoxP6tleiraw"
SHEET_NAME = "Sheet1"

def fetch_google_sheets_data():
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{SHEET_NAME}?key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Extract values and convert to JSON
        values = data.get("values", [])
        if not values or len(values) < 2:
            raise HTTPException(status_code=500, detail="No data found in sheet")

        headers = values[0]  # First row as headers
        items = [dict(zip(headers, row)) for row in values[1:]]  # Convert rows into JSON

        return items

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/items")
def get_items():
    return fetch_google_sheets_data()
# Run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


