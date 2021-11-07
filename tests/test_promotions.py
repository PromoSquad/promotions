import os
import logging
import unittest
from service.models import Promotion, PromotionType, DataValidationError, db, datetimeFormat
from service import app
from .factories import PromotionFactory
from datetime import datetime

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

class TestPromotionModel(unittest.TestCase):
    """ Promotion Model Tests """

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Promotion.init_db(app)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_promotion(self):
        promotion = Promotion(name="amazing", type=PromotionType.Percentage, description="99% off, almost free!", meta='{"percentOff": 0.99}',active=True)
        self.assertTrue(promotion != None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, "amazing")
        self.assertEqual(promotion.type, PromotionType.Percentage)
        self.assertEqual(promotion.description, "99% off, almost free!")
        self.assertEqual(promotion.meta, '{"percentOff": 0.99}')
        self.assertTrue(promotion.active)

    def test_add_a_promotion(self):
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = Promotion(name="amazing", type=PromotionType.Percentage, description="99% off, almost free!", meta='{"percentOff": 0.99}',active=True)
        self.assertTrue(promotion != None)
        self.assertEqual(promotion.id, None)
        promotion.create()
        self.assertEqual(promotion.id, 1)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_update_a_promotion(self):
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.create()
        logging.debug(promotion)
        self.assertEqual(promotion.id, 1)
        original_id = promotion.id
        promotion.type = PromotionType.Coupon
        promotion.meta = '{"dollarsOff": 10}'
        promotion.update()
        self.assertEqual(promotion.id, original_id)
        self.assertEqual(promotion.type, PromotionType.Coupon)
        self.assertEqual(promotion.meta, '{"dollarsOff": 10}')

    def test_delete_a_promotion(self):
        promotion = PromotionFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_serialize_a_promotion(self):
        promotion = PromotionFactory()
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)
        self.assertEqual(data["product_id"], promotion.product_id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        self.assertIn("type", data)
        self.assertEqual(data["type"], promotion.type.value)

        self.assertIn("description", data)
        self.assertEqual(data["description"], promotion.description)
        self.assertIn("meta", data)
        self.assertEqual(data["meta"], promotion.meta)
        self.assertIn("begin_date", data)
        self.assertEqual(data["begin_date"], promotion.begin_date.strftime(datetimeFormat))
        if not promotion.end_date:
            self.assertEqual(data["end_date"], None)
        else:
            self.assertEqual(data["end_data"], promotion.end_date.strftime(datetimeFormat))
        self.assertIn("active", data)
        self.assertEqual(data["active"], promotion.active)

    def test_deserialize_a_promotion(self):
        data = {
            "id": 1,
            "product_id": 5,
            "name": "amazing",
            "type": "coupon",
            "description": "this is amazing",
            "meta": '{"dollarsOff": 10}',
            "begin_date": "18-Nov-2018 (08:34:58.674035)",
            "end_date": "30-Dec-2021 (18:59:32.102939)",
            "active": True
        }
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.product_id, 5)
        self.assertEqual(promotion.name, "amazing"),
        self.assertEqual(promotion.type.value, "coupon"),
        self.assertEqual(promotion.description, "this is amazing")
        self.assertEqual(promotion.meta, '{"dollarsOff": 10}')
        self.assertEqual(promotion.begin_date, datetime.strptime("18-Nov-2018 (08:34:58.674035)", datetimeFormat))
        self.assertEqual(promotion.end_date, datetime.strptime("30-Dec-2021 (18:59:32.102939)", datetimeFormat))
        self.assertEqual(promotion.active, True)

    def test_deserialize_missing_data(self):
        data = {}
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["name"] = "amazing"
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["type"] = "coupon"
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["meta"] = '{"dollarsOff": 10}'
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["begin_date"] = '18-Nov-2018 (08:34:58.674035)'
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["active"] = True
        try:
            promotion.deserialize(data)
        except DataValidationError as error:
            self.assertEqual("should not have: " + str(error.args[0]), 0)

    def test_descrializing_bad_data(self):
        data = {
            "name": ""
        }
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["product_id"] = "sadsad"
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["product_id"] = "5"
        data["name"] = "amazing"
        data["type"] = "unknown type"
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["type"] = "percentage"
        data["meta"] = ''
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["type"] = "percentage"
        data["meta"] = '{"dollarsOff": 10}'
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["type"] = "coupon"
        data["meta"] = '{"percentage": 0.2}'
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["type"] = "bogo"
        data["meta"] = '{"percentage": 0.2}'
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["meta"] = '{"buy": 1}'
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["meta"] = '{"buy": 1, "get": 2}'

        data["begin_date"] = '18-Nov--2018 (08:34:58.674035)'
        self.assertRaises(DataValidationError, promotion.deserialize, data)

        data["begin_date"] = '18-Nov-2018 (08:34:58.674035)'

        data["end_date"] = '18-Nov--2018 (08:34:58.674035)'
        self.assertRaises(DataValidationError, promotion.deserialize, data)
        data["end_date"] = '18-Nov-2018 (08:34:58.674035)'

        data["active"] = True
        try:
            promotion.deserialize(data)
        except DataValidationError as error:
            self.assertEqual("should not have: " + str(error.args[0]), 0)

    def test_find_promotion(self):
        promotions = PromotionFactory.create_batch(3)
        for promotion in promotions:
            promotion.create()
        logging.debug(promotions)
        self.assertEqual(len(Promotion.all()), 3)
        promotion = Promotion.find(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.name, promotions[1].name)
        self.assertEqual(promotion.active, promotions[1].active)

    def test_find_by_status(self):
        data1 = {
            "product_id": 5,
            "name": "amazing",
            "type": "coupon",
            "description": "this is amazing",
            "meta": '{"dollarsOff": 10}',
            "begin_date": "18-Nov-2018 (08:34:58.674035)",
            "end_date": "30-Dec-2021 (18:59:32.102939)",
            "active": True
        }
        data2 = {
            "name": "amazing2",
            "type": "coupon",
            "description": "this is amazing2",
            "meta": '{"dollarsOff": 20}',
            "begin_date": "18-Nov-2018 (08:34:58.674035)",
            "active": False
        }
        data3 = {
            "name": "amazing3",
            "type": "percentage",
            "description": "this is amazing3",
            "meta": '{"percentOff": 0.2}',
            "begin_date": "18-Nov-2019 (08:34:58.674035)",
            "active": True
        }
        promotion1 = Promotion()
        promotion1.deserialize(data1).create()
        promotion2 = Promotion()
        promotion2.deserialize(data2).create()
        promotion3 = Promotion()
        promotion3.deserialize(data3).create()
        promotions = Promotion.find_by_status(True)
        self.assertEqual(len(promotions), 2)
        self.assertEqual(promotions[0].id, promotion1.id)
        self.assertEqual(promotions[1].id, promotion3.id)
        promotions = Promotion.find_by_status(False)
        self.assertEqual(len(promotions), 1)
