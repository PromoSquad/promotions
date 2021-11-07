import factory
from factory.declarations import LazyAttribute
from factory.fuzzy import FuzzyChoice
import random
from service.models import Promotion, PromotionType
import datetime

def generate_meta(promotionObj) -> str:
  if promotionObj.type == PromotionType.Percentage:
    return '{"percentOff": %.2f}' % (random.random())
  elif promotionObj.type == PromotionType.Coupon:
    return '{"dollarsOff": %.2f}' % (random.uniform(2.5, 100))
  elif promotionObj.type == PromotionType.BOGO:
    buy = random.randrange(1, 5)
    get = random.randrange(buy + 1, (buy + 1) * 2)
    return '{"buy": %d, "get": %d}' % (buy, get)
  raise Exception("Unknown promotion type: {}".format(promotionObj.type))

class PromotionFactory(factory.Factory):
  class Meta:
    model = Promotion
  id = factory.Sequence(lambda n : n)
  name = factory.Faker("catch_phrase")
  product_id = FuzzyChoice(choices=[None, 1, 2 ,3 , 4 ,5])
  type = FuzzyChoice(choices=[PromotionType.Percentage, PromotionType.Coupon, PromotionType.BOGO])
  description = factory.Faker("text")
  meta = LazyAttribute(generate_meta)
  begin_date = factory.LazyFunction(datetime.datetime.now)
  active = FuzzyChoice(choices=[True, False])
