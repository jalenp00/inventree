from fastapi import FastAPI
from routers import items, boms, inventory
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Inventree API")

# Allowed origins — adjust as needed
origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],            # or list like ["GET", "POST"]
    allow_headers=["*"],            # or restrict specific headers
)

app.include_router(items.router)
app.include_router(boms.router)
app.include_router(inventory.router)

@app.get("/")
async def root():
    return {"status": "ok"}
