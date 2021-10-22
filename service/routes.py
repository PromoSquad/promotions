from . import app
from .models import Promotion
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status

@app.route('/')
def index():
    return (
        jsonify(
            name="Promotion REST API Service",
            version="1.0"
        ),
        status.HTTP_200_OK
    )

def init_db():
    """ Initialize the SQLAlchemy app """
    global app
    Promotion.init_db(app)
