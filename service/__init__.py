import sys
import logging
from flask import Flask

app = Flask(__name__, static_url_path='', static_folder='static')
app.config.from_object("config")

from service import routes, models, error_handlers

print(f"Setting log level to {logging.INFO}")
app.logger.setLevel(logging.INFO)
app.logger.propagate = False

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
)

for handler in app.logger.handlers:
    handler.setFormatter(formatter)
app.logger.info("Logging handler established")

app.logger.info(70 * "*")
app.logger.info("  PROMOTIONS SERVICE RUNNING  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    routes.init_db()
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
