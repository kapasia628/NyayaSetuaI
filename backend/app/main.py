"""
Main Application Entrypoint for NyayaSetu AI.
Enterprise-grade Legal Assistance & Access Platform.
Unified architecture supporting local Uvicorn, Docker, and Vercel Serverless.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, Response
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

def get_static_content(filename: str) -> str:
    """
    Safely reads static assets across backend package, root, and frontend directories.
    Guaranteed to never raise an unhandled file system exception in serverless runtimes.
    """
    candidates = [
        os.path.join(os.path.dirname(__file__), "static", filename),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", filename)),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", filename)),
        os.path.abspath(filename)
    ]
    for p in candidates:
        if os.path.exists(p) and os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return ""

# Safe HTML and Asset Handlers (Zero 500s on Vercel Serverless)
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/index.html", response_class=HTMLResponse, include_in_schema=False)
async def serve_root():
    content = get_static_content("index.html")
    if content:
        return HTMLResponse(content=content, status_code=200)
    return HTMLResponse(content="<h1>NyayaSetu AI is running. Visit /docs for API.</h1>", status_code=200)

@app.get("/styles.css", include_in_schema=False)
async def serve_styles():
    content = get_static_content("styles.css")
    return Response(content=content, media_type="text/css")

@app.get("/app.js", include_in_schema=False)
async def serve_app_js():
    content = get_static_content("app.js")
    return Response(content=content, media_type="application/javascript")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
