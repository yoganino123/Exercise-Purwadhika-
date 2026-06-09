import fastapi

app = fastapi.FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/multiply")
async def multiply_numbers(x: float, y: float):
    return {"result": f"{x} * {y} = {x * y}"}

@app.post("/chatbot")
async def chatbot(message: str):
    response_chatbot = f"Echo: {message}\n Thanks for chatting!"
    return {"response": response_chatbot}