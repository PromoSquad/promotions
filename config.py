"""
Global Configuration for Application
"""
import os
import json # youngil
import logging # youngil

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "oi3k0az")
# LOGGING_LEVEL = logging.INFO # youngil
