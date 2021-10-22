import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Promotion(db.Model):
#     app: Flask = None

#     id = db.Column(db.Integer, primary_key = True)
