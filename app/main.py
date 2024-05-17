from fastapi import FastAPI
from app.api.router import api_router
from app.database import Database
from middlewares.locale import LocaleMiddleware

app = FastAPI()
app.add_middleware(LocaleMiddleware)

@app.on_event("startup")
async def startup_event():
    await Database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await Database.disconnect()

app.include_router(api_router)