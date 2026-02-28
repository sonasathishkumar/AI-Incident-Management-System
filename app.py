from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware   # ✅ ADD THIS

from api.routes import router

# 🔥 Database imports
from database.database import engine
from database.models import Base

# 🔥 Exception handlers
from exceptions.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

# ==============================
# Create FastAPI App
# ==============================
app = FastAPI(
    title="Incident AI System",
    description="AI-powered incident management system",
    version="1.0.0"
)

# ==============================
# ✅ CORS MIDDLEWARE (FIXES FAILED TO FETCH)
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Create Database Tables
# ==============================
Base.metadata.create_all(bind=engine)

# ==============================
# Register Global Exception Handlers
# ==============================
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Incident AI System is up and running 🚀"
    }

# ----------------------------
# Health check endpoint
# ----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# ----------------------------
# Include API routes
# ----------------------------
app.include_router(router)