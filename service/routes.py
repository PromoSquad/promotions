from . import app
from .models import Promotion

@app.route('/')
def index():
    return "<p>Hello, World2!</p>"

def init_db():
    """ Initialize the SQLAlchemy app """
    global app
    Promotion.init_db(app)
