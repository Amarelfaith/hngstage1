from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n: int) -> bool:
    return n == sum(i for i in range(1, n) if n % i == 0)


def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n


def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}")
        return response.text if response.status_code == 200 else "No fact available."
    except:
        return "No fact available."


@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to analyze")):
    if not isinstance(number, int):
        return {"number": number, "error": True}

    properties = []
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    if is_armstrong(number):
        properties.append("armstrong")

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(number)),
        "fun_fact": get_fun_fact(number)
    }
