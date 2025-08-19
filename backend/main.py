from fastapi import FastAPI
from routers import items, boms

app = FastAPI(title="Inventree API")

app.include_router(items.router)
app.include_router(boms.router)

@app.get("/")
async def root():
    return {"status": "ok"}
