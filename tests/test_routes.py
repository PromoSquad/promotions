import os
import logging
import unittest
from service import status
from service.models import Promotion, db, datetimeFormat
from service.routes import app, init_db
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = '/promotions'


class TestPromotionServer(unittest.TestCase):
    """ Promotion Server Tests """

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_promotions(self, count):
        promotions = []
        for i in range(count):
            test_promotion = PromotionFactory()
            if i == 0:
                test_promotion.product_id = 1
            resp = self.app.post(
                BASE_URL, json=test_promotion.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test promotion"
            )
            new_promotion = resp.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Promotion REST API Service")

    def test_get_promotion_list(self):
        """ Get a list of Promotions """
        self._create_promotions(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_query_promotion_list_by_status(self):
        promotions = self._create_promotions(10)
        active_promotions = [p for p in promotions if p.active]
        resp = self.app.get(
            BASE_URL, query_string="status=active"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(active_promotions))
        for promotion in data:
            self.assertEqual(promotion["active"], True)

    def test_query_promotion_list_by_productId(self):
        promotions = self._create_promotions(20)
        test_productId = promotions[0].product_id
        productId_promotions = [p for p in promotions if p.product_id == test_productId]
        resp = self.app.get(
            BASE_URL, query_string="productId={}".format(str(test_productId))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(productId_promotions))
        for promotion in data:
            self.assertEqual(promotion["product_id"], test_productId)

    def test_get_promotion(self):
        test_promotion = self._create_promotions(1)[0]
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_promotion.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_promotion.name)

    def test_get_promotion_not_found(self):
        resp = self.app.get("{}/0".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_promotion(self):
        test_promotion = PromotionFactory()
        logging.debug(test_promotion)
        resp = self.app.post(
            BASE_URL, json=test_promotion.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        new_promotion = resp.get_json()
        self.assertEqual(new_promotion["product_id"], test_promotion.product_id)
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(new_promotion["type"], test_promotion.type.value)
        self.assertEqual(new_promotion["description"], test_promotion.description)
        self.assertEqual(new_promotion["meta"], test_promotion.meta)
        self.assertEqual(new_promotion["begin_date"], test_promotion.begin_date.strftime(datetimeFormat))
        if "end_date" in new_promotion and new_promotion["end_date"] != None:
            self.assertEqual(new_promotion["end_date"], test_promotion.begin_date.strftime(datetimeFormat))
        self.assertEqual(new_promotion["active"], test_promotion.active)
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_promotion = resp.get_json()
        self.assertEqual(new_promotion["product_id"], test_promotion.product_id)
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(new_promotion["type"], test_promotion.type.value)
        self.assertEqual(new_promotion["description"], test_promotion.description)
        self.assertEqual(new_promotion["meta"], test_promotion.meta)
        self.assertEqual(new_promotion["begin_date"], test_promotion.begin_date.strftime(datetimeFormat))
        if "end_date" in new_promotion and new_promotion["end_date"] != None:
            self.assertEqual(new_promotion["end_date"], test_promotion.begin_date.strftime(datetimeFormat))
        self.assertEqual(new_promotion["active"], test_promotion.active)

    def test_create_promotion_with_wrong_content_type(self):
        test_promotion = PromotionFactory()
        logging.debug(test_promotion)
        resp = self.app.post(
            BASE_URL, json=test_promotion.serialize(), content_type="application/text"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_with_no_data(self):
        resp = self.app.post(
            BASE_URL, json={}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_with_wrong_method(self):
        test_promotion = PromotionFactory()
        logging.debug(test_promotion)
        resp = self.app.put(
            BASE_URL, json=test_promotion.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_delete_promotion(self):
        """ Delete a Promotion """
        test_promotion = self._create_promotions(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_promotion.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{}/{}".format(BASE_URL, test_promotion.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_promotion(self):
        """ Update an existing Promotion """
        # create a promotion to update
        test_promotion = PromotionFactory()
        resp = self.app.post(
            BASE_URL, json=test_promotion.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the promotion
        new_promotion = resp.get_json()
        logging.debug(new_promotion)
        new_promotion["description"] = "unknown"
        resp = self.app.put(
            "{0}/{1}".format(BASE_URL, new_promotion["id"]),
            json=new_promotion,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_promotion = resp.get_json()
        self.assertEqual(updated_promotion["description"], "unknown")

    def test_update_promotion_not_found(self):
        """ Update a product that's not found """
        test_promotion = PromotionFactory()
        resp = self.app.put(
            "/promotions/0",
            json=test_promotion.serialize(),
            content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

