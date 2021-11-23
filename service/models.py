from datetime import datetime
import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json

logger = logging.getLogger("flask.app")

db = SQLAlchemy()

datetimeFormat = "%d-%b-%Y (%H:%M:%S.%f)"

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class PromotionType(Enum):
  Percentage = "percentage"
  Coupon = "coupon"
  BOGO = "bogo"

class Promotion(db.Model):
  app: Flask = None

  id = db.Column(db.Integer(), primary_key = True)
  product_id = db.Column(db.Integer(), nullable = True)
  name = db.Column(db.String(63), nullable = False)
  type = db.Column(db.Enum(PromotionType), nullable = False)
  description = db.Column(db.Text(), nullable = True)
  meta = db.Column(db.Text, nullable = False)
  begin_date = db.Column(db.DateTime(), nullable = False, default=func.now())
  end_date = db.Column(db.DateTime(), nullable = True)
  active = db.Column(db.Boolean(), nullable = False)

  def __repr__(self) -> str:
    return "<Promotion id={} name={}>".format(self.id, self.name)

  def create(self):
    logger.info("Creating %s", self.name)
    self.id = None
    db.session.add(self)
    db.session.commit()

  def update(self):
    logger.info("Saving %s", self.name)
    db.session.commit()

  def delete(self):
    logger.info("Deleting %s", self.name)
    db.session.delete(self)
    db.session.commit()

  def serialize(self):
    return {
      "id": self.id,
      "product_id": self.product_id,
      "name": self.name,
      "type": self.type.value,
      "description": self.description,
      "meta": self.meta,
      "begin_date": self.begin_date.strftime(datetimeFormat),
      "end_date": self.end_date.strftime(datetimeFormat) if self.end_date else None,
      "active": self.active
    }

  def deserialize(self, data: dict):
    try:
      if "product_id" in data and data["product_id"] != None:
        try:
          self.product_id = int(data["product_id"])
        except ValueError:
          raise AttributeError("malformed product_id")
      else:
        self.product_id = None
      name = str(data["name"])
      if not name:
        raise AttributeError("name cannot be empty")
      self.name = name
      type = str(data["type"])
      if type not in [t.value for t in PromotionType]:
        raise AttributeError("unknown type `%s`" % (type))
      self.type = PromotionType(type)
      if "description" in data and data["description"] != None:
        self.description = str(data["description"])
      else:
        self.description = None
      meta = str(data["meta"])
      try:
        metaObj = json.loads(meta)
        if self.type == PromotionType.Percentage:
          if "percentOff" not in metaObj:
            raise AttributeError("meta must include `percentOff` for percentage promotion")
        elif self.type == PromotionType.Coupon:
          if "dollarsOff" not in metaObj:
            raise AttributeError("meta must include `dollarsOff` for percentage promotion")
        elif self.type == PromotionType.BOGO:
          if "buy" not in metaObj:
            raise AttributeError("meta must include `buy` for percentage BOGO promotion")
          elif "get" not in metaObj:
            raise AttributeError("meta must include `get` for percentage BOGO promotion")
      except json.decoder.JSONDecodeError:
        raise AttributeError("malformed meta")
      self.meta = meta
      try:
        self.begin_date = datetime.strptime(data["begin_date"], datetimeFormat)
      except ValueError:
        raise AttributeError("malformed begin_date")
      if "end_date" in data and data["end_date"] != None:
        try:
          self.end_date = datetime.strptime(data["end_date"], datetimeFormat)
        except ValueError:
          raise AttributeError("malformed end_date")
      else:
        self.end_date = None
      self.active = bool(data["active"])
    except AttributeError as error:
      raise DataValidationError("Invalid attribute: " + error.args[0])
    except KeyError as error:
      raise DataValidationError("Invalid promotion: missing " + error.args[0])
    return self

  @classmethod
  def init_db(cls, app: Flask):
    logger.info("Initializing database")
    cls.app = app
    db.init_app(app)
    app.app_context().push()
    db.create_all()

  @classmethod
  def all(cls):
    logger.info("Processing all Pets")
    return cls.query.all()

  @classmethod
  def find(cls, id: int):
    logger.info("Processing lookup for id %s ...", id)
    return cls.query.get(id)

  @classmethod
  def find_by_name(cls, name: str):
    logger.info("Processing lookup for name %s ...", name)
    return cls.query.filter_by(name=name).all()

  @classmethod
  def find_by_productId(cls, productId: int):
    """Returns all Promotions with the given product_id
    Args:
        product_id (int): the product_id of the Promotions you want to match """
    logger.info("Processing product_id query for %s ...", productId)
    return cls.query.filter_by(product_id=productId).all()

  @classmethod
  def find_by_status(cls, status: bool):
    logger.info("Processing lookup for status %s ...", status)
    return cls.query.filter_by(active=status).all()
