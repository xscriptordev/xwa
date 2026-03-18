from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from api.db.database import engine
from sqlmodel import SQLModel
from api.routers import scan, reports

app = FastAPI(
    title="xwa - Web Analysis Dashboard API",
    description="Backend API for managing SEO, Sitemap, and Security scans.",
    version="1.0.0"
)

# Optional: We will use Alembic for migrations, but this ensures tables exist
# if someone runs the app without running migrations first.
SQLModel.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(scan.router, prefix="/api", tags=["Scanner"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])

@app.get("/")
def root():
    return {"message": "xwa API is running"}
