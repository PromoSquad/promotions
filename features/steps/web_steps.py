"""
Web Steps

Steps file for web interactions with Selenium.
"""
import logging
import re
from behave import when, then
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

def format_as_id(text):
    return text.lower().replace(' ', '-')

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

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
  """ Set the value of an input field """
  element_id = 'input-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  element.clear()
  element.send_keys(text_string)

@when('I set the "{element_name}" empty')
def step_impl(context, element_name):
  """ Set the value of an input field empty"""
  element_id = 'input-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  element.clear()

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
  element_id = 'select-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  select = Select(element)
  select.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
  element_id = 'select-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  select = Select(element)
  expect(select.first_selected_option.text).to_equal(text)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
  element_id = 'input-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  expect(element.get_attribute('value')).to_equal('')

@when('I copy the Promotion ID in the message to the clipboard')
def step_impl(context):
  """Copy promotion ID from message in div with id "alert-message"""
  message = context.driver.find_element_by_id('alert-message').text
  message = message.strip()
  logging.info('Copying promotion ID from message: %s', message)
  result = re.match(r'^Promotion(\s+)(\d+)(\s+)', message)
  expect(result).to_be_truthy()
  id = result.group(2)
  context.clipboard = id

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
  element_id = 'input-' + format_as_id(element_name)
  element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
    expected_conditions.presence_of_element_located((By.ID, element_id))
  )
  element.clear()
  element.send_keys(context.clipboard)

@when('I press the "{element_name}" button')
def step_impl(context, element_name):
  element_id = 'button-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  context.driver.execute_script("arguments[0].click();", element)

@then('I should see message containing "{message}"')
def step_impl(context, message):
  """Check message in div with id "alert-message"""
  found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
    expected_conditions.text_to_be_present_in_element( (By.ID, 'alert-message'), message)
  )
  element = context.driver.find_element_by_id('alert-message')
  logging.info('Found message: %s', element.text)
  expect(found).to_be_truthy()

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
  element_id = 'input-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  expect(element.get_attribute('value')).to_equal(text_string)

@then('I should be in search mode')
def step_impl(context):
  """Radio with id 'radio-name' visible indicates search mode"""
  found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
    expected_conditions.visibility_of_element_located((By.ID, 'radio-name'))
  )
  expect(found).to_be_truthy()

@when('I check the "{element_name}" radio')
def step_impl(context, element_name):
  element_id = 'radio-' + format_as_id(element_name)
  element = context.driver.find_element_by_id(element_id)
  element.click()

@then('I should see "{text_string}" in the results')
def step_impl(context, text_string):
  """results are in div with id 'promotion-list'"""
  found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
    expected_conditions.text_to_be_present_in_element( (By.ID, 'promotion-list'), text_string)
  )
  expect(found).to_be_truthy()

@then('I should not see "{text_string}" in the results')
def step_impl(context, text_string):
  element = context.driver.find_element_by_id('promotion-list')
  error_msg = "I should not see '{}' in '{}'".format(text_string, element.text)
  ensure(text_string in element.text, False, error_msg)
