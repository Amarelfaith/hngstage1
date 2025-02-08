from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import is_armstrong, is_perfect, is_prime, digit_sum
import httpx

app = FastAPI(
    title="Number Classification API",
    description="An API that classifies a number with its properties and provides a fun fact.",
    version="1.0.0"
)

# Enable CORS for all origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API endpoint
@app.get("/api/classify-number", status_code=200)
async def classify_number(number: str = Query(..., description="The number to classify")):

    try:
        n = int(number)
    except ValueError:
        return JSONResponse(status_code=400, content={"number": number, "error": True})
    
    # Determine properties
    prime = is_prime(n)
    perfect = is_perfect(n)
    armstrong = is_armstrong(n)
    parity = "even" if abs(n) % 2 == 0 else "odd"
    
    properties = []
    if armstrong:
        properties.append("armstrong")
    properties.append(parity)
    
    dsum = digit_sum(n)
    
    # Get fun fact from the Numbers API (e.g., http://numbersapi.com/371?json)
    fun_fact = ""
    try:
        async with httpx.AsyncClient() as client:
            url = f"http://numbersapi.com/{n}/math?json"
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                fun_fact = data.get("text", "No fun fact available.")
            else:
                fun_fact = "No fun fact available."
    except Exception:
        fun_fact = "No fun fact available."
    
    return {
        "number": n,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": dsum,
        "fun_fact": fun_fact
    }