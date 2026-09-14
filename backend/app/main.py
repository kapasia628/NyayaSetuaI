"""
Main Application Entrypoint for NyayaSetu AI.
Enterprise-grade Legal Assistance & Access Platform.
Supports local execution, Docker containers, and Vercel serverless deployments.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
import time

from app.core.config import settings
from app.api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers & Latency Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # OWASP Recommended Security Headers
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Register API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

def resolve_static_path(filename: str) -> str:
    """Finds the absolute path of a static file across root and frontend directories."""
    candidates = [
        os.path.abspath(filename),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", filename)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", filename)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
    ]
    for candidate in candidates:
        if os.path.exists(candidate) and os.path.isfile(candidate):
            return candidate
    return filename

# Static UI File Routes (Guarantees zero 404s on Vercel Serverless)
@app.get("/", include_in_schema=False)
async def serve_root():
    return FileResponse(resolve_static_path("index.html"), media_type="text/html")

@app.get("/index.html", include_in_schema=False)
async def serve_index_html():
    return FileResponse(resolve_static_path("index.html"), media_type="text/html")

@app.get("/styles.css", include_in_schema=False)
async def serve_styles():
    return FileResponse(resolve_static_path("styles.css"), media_type="text/css")

@app.get("/app.js", include_in_schema=False)
async def serve_app_js():
    return FileResponse(resolve_static_path("app.js"), media_type="application/javascript")

# Fallback mount for any extra static assets
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
