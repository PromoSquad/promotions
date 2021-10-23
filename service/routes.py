from flask.signals import message_flashed
from werkzeug.exceptions import NotFound
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

@app.route('/promotions/<int:id>', methods=["GET"])
def get_promotions(id):
    app.logger.info("Request for promotion with id: %s", id)
    promotion = Promotion.find(id)
    if not promotion:
        raise NotFound("Promotion with id '{}' was not found.".format(id))
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)

@app.route('/promotions', methods=["POST"])
def create_promotions():
    app.logger.info("Request to create a promotion")
    check_content_type("application/json")
    promotion = Promotion()
    promotion.deserialize(request.get_json())
    promotion.create()
    message = promotion.serialize()
    location_url = url_for("get_promotions", id=promotion.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"location": location_url}
    )

def init_db():
    """ Initialize the SQLAlchemy app """
    global app
    Promotion.init_db(app)

def check_content_type(content_type):
    if "Content-Type" in request.headers and request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: [%s]", request.headers.get("Content-Type"))
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be {}".format(content_type))
