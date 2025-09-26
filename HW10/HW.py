from typing import Any, Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_key = "XZPBF7J8PYDXQV8U"

class Price:
    def __init__(self, amount: float, currency: str):
        self.amount: float = amount
        self.currency: str = currency

    def __add__(self, other: Any):
        if not isinstance(other, Price):
            raise ValueError('Can perform operations only with "Price" objects')
        else:
            if self.currency != other.currency:
                url1 = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={self.currency}&to_currency=CHF&apikey={API_key}'
                url2 = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={other.currency}&to_currency=CHF&apikey={API_key}'

                r1 = requests.get(url1).json()
                r2 = requests.get(url2).json()

                rate1 = float(r1["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
                rate2 = float(r2["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

                amount_chf = self.amount * rate1 + other.amount * rate2

                url_back = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=CHF&to_currency={self.currency}&apikey={API_key}'
                r_back = requests.get(url_back).json()
                back_rate = float(r_back["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

                final_amount = round(amount_chf * back_rate, 2)

                return Price(final_amount, self.currency)
            else:
                return Price(self.amount + other.amount, self.currency)
    def __sub__(self, other: Any):
        if not isinstance(other, Price):
            raise ValueError('Can perform operations only with "Price" objects')
        else:
            if self.currency != other.currency:
                url1 = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={self.currency}&to_currency=CHF&apikey={API_key}'
                url2 = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={other.currency}&to_currency=CHF&apikey={API_key}'

                r1 = requests.get(url1).json()
                r2 = requests.get(url2).json()

                rate1 = float(r1["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
                rate2 = float(r2["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

                amount_chf = self.amount * rate1 - other.amount * rate2

                url_back = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=CHF&to_currency={self.currency}&apikey={API_key}'
                r_back = requests.get(url_back).json()
                back_rate = float(r_back["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

                final_amount = round(amount_chf * back_rate, 2)

                return Price(final_amount, self.currency)
            else:
                return Price(self.amount - other.amount, self.currency)

class Data(BaseModel):
    a: str
    b: str
    sign: Literal["+", "-"]

@app.post('/calculate')
def calculate(data: Data):
    try:
        a_amount, a_currency = data.a.strip().split(" ")
        b_amount, b_currency = data.b.strip().split(" ")

        price_a = Price(float(a_amount), a_currency)
        price_b = Price(float(b_amount), b_currency)

        if data.sign == "+":
            result = price_a + price_b
        else:
            result = price_a - price_b
        
        return {"result": f"{result.amount} {result.currency}"}
    
    except ValueError as e:
        return {"result": str(e)}
    except Exception:
        return {"result": "Invalid input format. Use format like '100 USD'"}
