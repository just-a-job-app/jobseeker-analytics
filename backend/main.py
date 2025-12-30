import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from guard import SecurityMiddleware, SecurityConfig, GeoIPHandler
from utils.config_utils import get_settings
from contextlib import asynccontextmanager

# Import routes
from routes import email_routes, auth_routes, file_routes, users_routes, start_date_routes, job_applications_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
settings = get_settings()
APP_URL = settings.APP_URL

# Configure session middleware with proper settings for production
if settings.is_publicly_deployed:
    app.add_middleware(
        SessionMiddleware, 
        secret_key=settings.COOKIE_SECRET,
        session_cookie="session",
        max_age=3600,
        same_site="lax",
        https_only=True,
        domain=settings.ORIGIN
    )
else:
    app.add_middleware(SessionMiddleware, secret_key=settings.COOKIE_SECRET)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routes
app.include_router(auth_routes.router)
app.include_router(email_routes.router)
app.include_router(file_routes.router)
app.include_router(users_routes.router)
app.include_router(start_date_routes.router)
app.include_router(job_applications_routes.router)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter  # Ensure limiter is assigned

# Add SlowAPI middleware for rate limiting
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.APP_URL, settings.API_URL],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#Add FastApi-Guard middleware for whitelisting only US IPs
if settings.is_publicly_deployed:
    config = SecurityConfig(
    geo_ip_handler=GeoIPHandler,
    ipinfo_token=settings.IPINFO_TOKEN,
    whitelist_countries=["US"]
    )
    app.add_middleware(SecurityMiddleware,config=config)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")


# Rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(
        status_code=429,
        detail="Too many requests. Please try again later.",
    )

@app.get("/")
async def root():
    return {"message": "success"}

@app.get("/heartbeat")
@limiter.limit("4/hour")
async def heartbeat(request: Request):
    """
    Lightweight endpoint to check if the backend is alive.
    No rate limiting applied to prevent blocking health checks.
    """
    return {"status": "alive", "timestamp": datetime.now().isoformat()}



# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)