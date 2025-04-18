# AutoDB
A web application to upload and manage customer and order data. This app allows users to upload CSV data for customers and orders, store it in a database, and interact with the data via API endpoints.

I have hosted a simple example on render: [https://autodb-2aua.onrender.com](https://autodb-2aua.onrender.com) 
<br>
I have example customer and order CSVs to upload as well in the repo.

---

## Table of Contents
- [Installation](#installation)
- [Endpoints](#endpoints)
  - [POST /upload](#post-upload)
  - [POST /query](#post-query)
  - [GET /data](#get-data)
- [Reasoning](#reasoning)
---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Tsangington/autodb
   cd autodb
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   ```bash
   windows: venv\Scripts\activate
   linux/mac: source venv/bin/activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Enter your ENV variables** - 
   (I used a postgres database)
   ```bash
   OPENAI_API_KEY=""
   DB_NAME=""
   DB_USER=""
   DB_PASSWORD=""
   DB_HOST=""
   DB_PORT=""
   ```
6. **To run locally:**
   ```bash
   python main.py
   ```
   
## Endpoints

### 1. `/upload`
**Method:** `POST`

This endpoint is used to upload to the customer or order tables. You can send either a JSON or CSV file containing customer information, such as their name and creation date.

#### Request:
- **Body:** A file (JSON or CSV) containing customer data.
  - For **JSON**: The file should be an array of customer objects with the following keys:
    - `name`: The name of the customer.
    - `created_at`: The timestamp when the customer was created.
  - For **CSV**: The file should contain two columns:
    - `name`: The name of the customer.
    - `created_at`: The timestamp when the customer was created.
    
### 2. `/data`
**Method:** `GET`

This endpoint retrieves all the customer and order data stored in the database.

#### Request:
- **Method:** `GET`
- **URL:** `/data`

### 3. `/query`
**Method:** `POST`

This endpoint allows you to send a question in the form of a string, and it will return an answer based on the available customer and order data.

#### Request:
- **Method:** `POST`
- **URL:** `/query`
- **Body:**
  - A `question` parameter (string) sent as form data.
  - The `question` parameter should be a text query asking about the data, such as "What is the total amount spent by customer Alice Johnson?" or "When did customer Bob Smith make a purchase?"

## Reasoning

- **Scalability** was a major factor in choosing PostgreSQL (mainly a relational database), as it handles large datasets efficiently compared to key-value stores or flat files like Excel sheets.
- **Structured Data** and the ability to define **relationships** between different data entities made a relational database the most appropriate choice for the application, and made it much easier to query. If we needed more unstructured data, a NoSQL database would also be much better than a key-value pair or an excel sheet.
- **Ease of Interaction** with data via **natural language processing** provided by ChatGPT enhances the user experience by making it more intuitive, allowing the user to have less technical knowledge to access data that they might need
