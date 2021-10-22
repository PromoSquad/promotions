from flask import Blueprint

routes = Blueprint('api', __name__)

from .index import *