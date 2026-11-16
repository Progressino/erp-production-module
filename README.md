# ERP Production Module

Standalone extraction of the **Production / Job Order / MRP** module from Yash Gallery ERP.

## What's included

| Layer | Files | Purpose |
|---|---|---|
| Backend DB | `backend/db/production_db.py` | Full SQLite schema + all CRUD for Job Orders, fabric issue/receive, MRP, embroidery, set-BOM, reservations |
| Backend DB | `backend/db/sales_db.py` | Sales Orders (SOs) — production reads open SOs for MRP |
| Backend DB | `backend/db/item_db.py` | Item Master / BOM — production reads SKU routing and BOMs |
| Backend router | `backend/routers/production.py` | All FastAPI endpoints: JO lifecycle, MRP, fabric movements, WIP board |
| Backend services | `backend/services/production_db.py` | — (see db layer) |
| Backend services | `backend/services/jo_import.py` | Bulk JO import from Excel/CSV template |
| Backend services | `backend/services/jo_issue_notes.py` | BOM-driven material issue notes |
| Backend services | `backend/services/component_bom.py` | Panel/set BOM logic |
| Backend services | `backend/services/set_components.py` | Set component SKU parsing |
| Backend services | `backend/services/helpers.py` | Shared SKU/data helpers |
| Backend services | `backend/services/so_production_path.py` | Production mode (inhouse/job-work) normalisation |
| Frontend | `frontend/src/pages/Production.tsx` | Full React production management UI |
| Frontend | `frontend/src/lib/productionEntrySave.ts` | Production entry save helpers |
| Tests | `tests/test_production_module_smoke.py` | Smoke tests: schema init, endpoint happy paths |
| Tests | `tests/test_so_production_path.py` | Unit tests for production mode logic |

## Production flow

```
Sales Order → Job Order (JO) → Cutting → Stitching → Embroidery → Finishing → Gate Inward
```

Each stage records: quantities processed, worker assignment, material issue/receive, and completion date.

## Quickstart

```bash
# 1. Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure paths (optional — defaults to local .db files)
cp .env.example .env

# 3. Run
uvicorn backend.main:app --reload --port 8000
```

API docs at: http://localhost:8000/docs

## Key API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/production/jo` | List all Job Orders |
| POST | `/api/production/jo` | Create a Job Order |
| GET | `/api/production/jo/{id}` | Get JO detail |
| POST | `/api/production/jo/{id}/issue-fabric` | Issue fabric to a JO |
| POST | `/api/production/jo/{id}/receive` | Receive output from a JO |
| GET | `/api/production/wip-board` | Current WIP board across all processes |
| POST | `/api/production/mrp/run` | Run MRP against open Sales Orders |
| GET | `/api/production/routing` | List all operation routing steps |
| POST | `/api/production/jo/import` | Bulk import JOs from Excel/CSV |

## Languages

- **Backend**: Python 3 (FastAPI, SQLite, pandas)
- **Frontend**: TypeScript / React (TSX)

## Dependencies

- No external database server required — SQLite only
- No warm cache, no PostgreSQL, no GitHub data pipeline
- Three `.db` files: `production.db`, `sales.db`, `items.db`
