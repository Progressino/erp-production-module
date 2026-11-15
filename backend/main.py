"""
Yash Gallery ERP — Production Module (standalone)

Runs the Production, Sales Orders, and Item Master endpoints as an
isolated FastAPI service. No dependency on the full ERP warm-cache or
PostgreSQL — only SQLite files are required.

Environment variables (all optional; defaults to local .db files):
    PRODUCTION_DB_PATH   path to production.db
    SALES_DB_PATH        path to sales.db
    ITEM_DB_PATH         path to items.db

Usage:
    uvicorn backend.main:app --reload --port 8000
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.production_db import init_db as init_production_db
from .db.sales_db import init_db as init_sales_db
from .db.item_db import init_db as init_item_db
from .routers.production import router as production_router

# Initialise schemas on startup (safe to call on existing DBs)
init_production_db()
init_sales_db()
init_item_db()

app = FastAPI(
    title="ERP Production Module",
    description="Standalone Production / Job Order / MRP service extracted from Yash Gallery ERP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(production_router, prefix="/api/production", tags=["production"])


@app.get("/api/health")
def health():
    return {"status": "ok", "module": "production"}
