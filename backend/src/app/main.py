from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import connect_db, disconnect_db
from routes import deals, templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(
    title="Deal Viewer API",
    description="Commercial deals management with display templates",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deals.router, prefix="/deals", tags=["Deals"])
app.include_router(templates.router, prefix="/templates", tags=["Templates"])

@app.get("/")
async def root():
    return {"message": "Deal Viewer API", "version": "1.0.0"}