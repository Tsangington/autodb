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

@app.post("/upload_customer")
async def upload_customer(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        data = json.loads(contents)
    except Exception:
        file.file.seek(0)
        df = pd.read_csv(file.file)
        data = df.to_dict(orient="records")

    for customer in data:
        name = customer.get("name")
        created_at = customer.get("created_at")
        if name:
            db.store_customer(name, created_at)
    return {"message": "Customer data uploaded successfully."}

@app.post("/upload_order")
async def upload_order(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        data = json.loads(contents)
    except Exception:
        file.file.seek(0)
        df = pd.read_csv(file.file)
        data = df.to_dict(orient="records")

    for order in data:
        customer_id = order.get("customer_id")
        price = order.get("price")
        order_date = order.get("order_date")
        if customer_id and price is not None:
            db.store_order(customer_id, price, order_date)
    return {"message": "Order data uploaded successfully."}

@app.get("/query", response_class=HTMLResponse)
async def form_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Ask a Question</title>
    </head>
    <body>
        <h1>Ask a Question</h1>
        <form action="/query" method="post">
            <input type="text" name="question" placeholder="Type your question here" required>
            <button type="submit">Ask</button>
        </form>
    </body>
    </html>
    """

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