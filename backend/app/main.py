from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import init_db
from app.api import ingest

app = FastAPI(title="MemRead API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(ingest.router, prefix="/v1")

@app.get("/")
async def root():
    return {"message": "MemRead API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
