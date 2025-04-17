from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from prompt import get_answer
import database 
import pandas as pd
import json
import os
import uvicorn
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

app = FastAPI()
db = database.Database(name=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

@app.get("/upload")
async def upload_form():
    with open("/static/html/upload.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/upload")
async def upload(file: UploadFile = File(...), table: str = Form(...)):
    contents = await file.read()
    try:
        data = json.loads(contents)
    except Exception:
        file.file.seek(0)
        df = pd.read_csv(file.file)
        data = df.to_dict(orient="records")

    if table == "customer":
        for customer in data:
            name = customer.get("name")
            created_at = customer.get("created_at")
            if name:
                db.store_customer(name, created_at)
    elif table == "order":
        for order in data:
            customer_id = order.get("customer_id")
            price = order.get("price")
            order_date = order.get("order_date")
            if customer_id and price:
                db.store_order(customer_id, price, order_date)
    else:
        return {"message": "Invalid table selected."}

    return {"message": f"{table.capitalize()} data uploaded successfully."}

@app.get("/query", response_class=HTMLResponse)
async def form_page():
    with open("/static/html/query.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/answer")
async def query(question: str = Form(...)):
    data = db.get_data()
    answer = get_answer(question, data)
    return {"answer": answer}

@app.get("/data")
async def get_data():
    return {"data": db.get_data()}

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)