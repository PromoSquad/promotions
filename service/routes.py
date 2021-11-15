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

######################################################################
# LIST ALL PROMOTIONS
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """ Returns all of the Promotions """
    app.logger.info("Request for promotion list")
    promotions = []
    query_status = request.args.get("status")
    query_productId = request.args.get("productId")
    if query_status:
        promotions = Promotion.find_by_status(query_status.lower()=="active")
    elif query_productId:
        promotions = Promotion.find_by_productId(query_productId)
    else:
        promotions = Promotion.all()

    results = [promotion.serialize() for promotion in promotions]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# DELETE A PROMOTION
######################################################################
@app.route("/promotions/<int:id>", methods=["DELETE"])
def delete_promotions(id):
    """
    Delete a Promotioon
    This endpoint will delete a Promotion based the id specified in the path
    """
    app.logger.info("Request to delete promotion with id: %s", id)
    promotion = Promotion.find(id)
    if promotion:
        promotion.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# UPDATE AN EXISTING PROMOTION
######################################################################
@app.route("/promotions/<int:id>", methods=["PUT"])
def update_promotions(id):
    """
    Update a Promotion
    This endpoint will update a Promotion based the body that is posted
    """
    app.logger.info("Request to update promotion with id: %s", id)
    check_content_type("application/json")
    promotion = Promotion.find(id)
    if not promotion:
        raise NotFound("Promotion with id '{}' was not found.".format(id))
    promotion.deserialize(request.get_json())
    promotion.id = id
    promotion.update()
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)

######################################################################
# UPDATE A PROMOTION TO ACTIVATE
######################################################################
@app.route("/promotions/<int:id>/activate", methods=["PUT"])
def activate_promotions(id):
    """
    Update a Promotion to activate
    This endpoint will update a Promotion's activate status based the body that is posted
    """
    app.logger.info("Request to update promotion with id: %s", id)
    check_content_type("application/json")
    promotion = Promotion.find(id)
    if not promotion:
        raise NotFound("Promotion with id '{}' was not found.".format(id))
    promotion.deserialize(request.get_json())
    promotion.active = True
    promotion.update()
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)

def init_db():
    """ Initialize the SQLAlchemy app """
    global app
    Promotion.init_db(app)

def check_content_type(content_type):
    if "Content-Type" in request.headers and request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: [%s]", request.headers.get("Content-Type"))
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be {}".format(content_type))
