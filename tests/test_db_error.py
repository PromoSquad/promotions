import logging
import unittest

from service.routes import app
from service.models import DatabaseConnectionError, Promotion
from service import app

DATABASE_URI = "postgres://random:pass@localhost:123/no_idea"

BASE_URL = '/promotions'

class TestDbError(unittest.TestCase):
  """ Database Error Tests """

  @classmethod
  def setUpClass(cls):
      app.config["TESTING"] = True
      app.config["DEBUG"] = False
      app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
      app.logger.setLevel(logging.CRITICAL)

  def test_invalid_database_url_with_model(self):
    self.assertRaises(DatabaseConnectionError, Promotion.init_db, app)
