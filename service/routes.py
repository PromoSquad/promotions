from . import app
from .models import Promotion, DataValidationError, DatabaseConnectionError
from flask import abort
from flask_restx import Api, Resource, fields, reqparse
from . import status

######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route('/')
def index():
    return app.send_static_file('index.html')

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
    version='1.0.0',
    title='Promotion REST API Service',
    description='A simple Promotion management REST API Service',
    default='promotions',
    default_label='Promotion management operations',
    doc='/apidocs'
)

# Define the model so that the docs reflect what can be sent
create_model = api.model('Promotion', {
    'name': fields.String(required=True, description='The name of the promotion'),
    'product_id': fields.Integer(required=False, description='The ID of the product this promotion is related to'),
    'active': fields.Boolean(required=True, description='Whether the promotion is active or not'),
    'description': fields.String(required=False, description='The description of the promotion'),
    'type': fields.String(required=True, description='The type of the promotion: "percentage", "coupon" or "bogo"'),
    'meta': fields.String(required=True, description='The meta data of the promotion, different format for different type of promotion'),
    'begin_date': fields.String(required=True, description='The begin date of the promotion'),
    'end_date': fields.String(required=False, description='The end date of the promotion')
})

promotion_model = api.inherit('PromotionModel', create_model, {
    'id': fields.String(readOnly=True, description='The unique id assigned internally by service'),
})

# query string arguments
promotion_args = reqparse.RequestParser()
promotion_args.add_argument('name', type=str, required=False, help='List Promotions by name')
promotion_args.add_argument('product_id', type=int, required=False, help='List Promotions by product_id')
promotion_args.add_argument('status', type=str, required=False, help='List Promotions by status')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Connection Errors """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_503_INTERNAL_SERVER_ERROR,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_INTERNAL_SERVER_ERROR

######################################################################
#  PATH: /promotions/{id}
######################################################################
@api.route('/promotions/<promotion_id>')
@api.param('promotion_id', 'The Promotion identifier')
class PromotionResource(Resource):
    """
    Promotion Resource
    """

    #------------------------------------------------------------------
    # RETRIEVE A PROMOTION
    #------------------------------------------------------------------
    @api.doc('get_promotions')
    @api.response(404, 'Promotion not found')
    @api.marshal_with(promotion_model)
    def get(self, promotion_id):
        app.logger.info("Request for promotion with id: %s", id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, "Promotion with id '{}' was not found.".format(promotion_id))
        return promotion.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING PROMOTION
    #------------------------------------------------------------------
    @api.doc('update_promotions')
    @api.response(404, 'Promotion not found')
    @api.response(400, 'The posted Promotion data was not valid')
    @api.expect(promotion_model)
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
        app.logger.info("Request to update promotion with id: %s", id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, "Promotion with id '{}' was not found.".format(promotion_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        promotion.deserialize(data)
        promotion.id = promotion_id
        promotion.update()
        return promotion.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE A PET
    #------------------------------------------------------------------
    @api.doc('delete_promotions')
    @api.response(204, 'Promotion deleted')
    def delete(self, promotion_id):
        app.logger.info("Request to delete promotion with id: %s", id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, "Promotion with id '{}' was not found.".format(promotion_id))
        promotion.delete()
        return '', status.HTTP_204_NO_CONTENT

######################################################################
#  PATH: /promotions
######################################################################
@api.route('/promotions', strict_slashes=False)
class PromotionCollection(Resource):
    """ Handles all interactions with collections of promotions """

    #------------------------------------------------------------------
    # READ ALL PROMOTIONS
    #------------------------------------------------------------------
    @api.doc('list_promotions')
    @api.expect(promotion_args, validate=True)
    @api.marshal_list_with(promotion_model)
    def get(self):
        """ Returns all promotions """
        app.logger.info("Request for list of promotions")
        promotions = []
        args = promotion_args.parse_args()
        if args['name']:
            app.logger.info("Filtering promotions by name: %s", args['name'])
            promotions = Promotion.find_by_name(args['name'])
        elif args['product_id']:
            app.logger.info("Filtering promotions by product_id: %s", args['product_id'])
            promotions = Promotion.find_by_product_id(args['product_id'])
        elif args['status']:
            app.logger.info("Filtering promotions by status: %s", args['status'])
            promotions = Promotion.find_by_status(args['status'].lower() == 'active')
        else:
            app.logger.info("Returning all promotions")
            promotions = Promotion.all()
        app.logger.info("Returning %s promotions", len(promotions))
        results = [promotion.serialize() for promotion in promotions]
        return results, status.HTTP_200_OK

    #------------------------------------------------------------------
    # CREATE A NEW PROMOTION
    #------------------------------------------------------------------
    @api.doc('create_promotions')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(promotion_model, code=201)
    def post(self):
        """ Create a new promotion """
        app.logger.info("Received request to create new promotion")
        promotion = Promotion()
        data = api.payload
        app.logger.debug("Payload = %s", data)
        promotion.deserialize(data)
        promotion.create()
        app.logger.info("Created promotion with id: %s", promotion.id)
        location_url = api.url_for(PromotionResource, promotion_id=promotion.id, _external=True)
        return promotion.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

######################################################################
#  PATH: /promotions/{id}/activate
######################################################################
@api.route('/promotions/<promotion_id>/activate')
@api.param('promotion_id', 'The Promotion identifier')
class PromotionActivateResource(Resource):
    """ Activate actions on a Promotion """
    @api.doc('activate_promotions')
    @api.response(404, 'Promotion not found')
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
        app.logger.info("Request to activate promotion with id: %s", id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, "Promotion with id '{}' was not found.".format(promotion_id))
        promotion.active = True
        promotion.update()
        return promotion.serialize(), status.HTTP_200_OK

######################################################################
#  PATH: /promotions/{id}/deactivate
######################################################################
@api.route('/promotions/<promotion_id>/deactivate')
@api.param('promotion_id', 'The Promotion identifier')
class PromotionDeactivateResource(Resource):
    """ Deactivate actions on a Promotion """
    @api.doc('deactivate_promotions')
    @api.response(404, 'Promotion not found')
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
        app.logger.info("Request to deactivate promotion with id: %s", id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(status.HTTP_404_NOT_FOUND, "Promotion with id '{}' was not found.".format(promotion_id))
        promotion.active = False
        promotion.update()
        return promotion.serialize(), status.HTTP_200_OK

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)

def init_db():
    """ Initialize the SQLAlchemy app """
    global app
    Promotion.init_db(app)
