from . import app

@app.route('/')
def index():
    return "<p>Hello, World2!</p>"
