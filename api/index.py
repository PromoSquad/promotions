from . import routes

@routes.route('/')
def index():
    return "<p>Hello, World2!</p>"