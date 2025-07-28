import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from db.users import UserData
from db.utils.user_utils import add_user
from utils.config_utils import get_settings
from session.session_layer import validate_session
from contextlib import asynccontextmanager
from database import create_db_and_tables
from db.utils.dev_utils import clear_local_database  # noqa: F401

# Import routes
from routes import email_routes, auth_routes, file_routes, users_routes, start_date_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    # Clear database in local development
    # clear_local_database()  # uncomment to clear database in local development
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

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

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


@app.post("/api/add-user")
@limiter.limit("3/minute")
async def add_user_endpoint(user_data: UserData, request: Request, user_id: str = Depends(validate_session)):
    """
    This endpoint adds a user to the database and session storage
    """
    try:
        add_user(user_data, request)
        return {"message": "User added successfully"}
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"An error occurred while adding user: {e}")
        return {"error": "An error occurred while adding the user."}


# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)