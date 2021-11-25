"""
Web Steps

Steps file for web interactions with Selenium.
"""
import logging
from behave import when, then
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

ID_PREFIX = 'promotion_'

@when('I visit the "Home Page"')
def step_impl(context):
  """ Make a call to the base URL """
  context.driver.get(context.base_url)
  logging.info('Visited the base URL: %s', context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
  """ Check the title of the page """
  expect(context.driver.title).to_contain(message)

@then('I should not see "{message}"')
def step_impl(context, message):
  error_msg = "I should not see '{}' in '{}'".format(message, context.resp.text)
  ensure(message in context.resp.text, False, error_msg)
