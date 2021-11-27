"""
Promotion Steps
"""
import json
import requests
from behave import given
from compare import expect

@given('the following promotions')
def step_impl(context):
  """ Delete all Promotions and load new ones """
  headers = {'Content-Type': 'application/json'}
  # list all promotions and delete them one by one
  context.resp = requests.get(context.base_url + '/promotions')
  expect(context.resp.status_code).to_equal(200)
  for promotion in context.resp.json():
    context.resp = requests.delete(context.base_url + '/promotions/' + str(promotion['id']), headers=headers)
    expect(context.resp.status_code).to_equal(204)

  # load new promotions
  create_url = context.base_url + '/promotions'
  for row in context.table:
    data = {
      'name': row['name'],
      'description': row['description'],
      'product_id': row['product_id'],
      'active': row['status'] == 'active',
      'type': row['type'],
      'meta': row['meta'],
      'begin_date': row['begin_date'],
      'end_date': row['end_date']
    }
    payload = json.dumps(data)
    context.resp = requests.post(create_url, data=payload, headers=headers)
    expect(context.resp.status_code).to_equal(201)
    if 'first_id' not in context:
      context.first_id = context.resp.json()['id']
