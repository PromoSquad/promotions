Feature: The promotions service back-end
  As a Marketing Manager
  I need a RESTful service to manage promotions
  So that I can keep track of all the promotions

Background:
  Given the following promotions:
    | name                            | description                                           | product_id | status   | type       | meta                 | begin_date                    | end_date                      |
    | Market Black Friday             | Amazing 20% discount on all purchases on Black Friday |            | active   | percentage | {"percentOff": 0.2}  | 26-Nov-2021 (00:00:00.000000) | 27-Nov-2021 (00:00:00.000000) |
    | Amazing Toaster Discount        | Amazing discount for high-end toasters!               | 15         | inactive | percentage | {"percentOff": 0.1}  | 18-Nov-2018 (08:00:00.000000) |                               |
    | MacBook Pro Discount            | 50% off on the new MacBook Pro!                       | 101        | active   | percentage | {"percentOff": 0.5}  | 26-Nov-2021 (00:00:00.000000) |                               |
    | Grand Theft Auto Trilogy Coupon | $10 off on your purchase of the new GTA Trilogy!      | 213        | active   | coupon     | {"dollarsOff": 10}   | 26-Nov-2021 (00:00:00.000000) |                               |
    | Chips Ahoy                      | Buy one get one free on chips!                        | 19         | active   | bogo       | {"buy": 1, "get": 2} | 26-Nov-2021 (00:00:00.000000) |                               |

Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Promotions RESTful Service Demo" in the title
  And I should not see "404 Not Found"

Scenario: Create a promotion
  When I visit the "Home Page"
  And I set the "Name" to "Cheese Burger Coupon"
  And I set the "Description" to "$5 off on your purchase of cheese burger"
  And I set the "Product ID" to "20"
  And I select "Active" in the "Status" dropdown
  And I select "Coupon" in the "Type" dropdown
  And I set the "Meta" to "{"dollarsOff": 5}"
  And I set the "Begin date" to "26-Nov-2021 (00:00:00.000000)"
  And I set the "End date" empty
  And I press the "Create" button
  Then I should see message containing "created successfully"
  When I copy the Promotion ID in the message to the clipboard
  And I press the "Reset" button
  Then the "Promotion ID" field should be empty
  And the "Name" field should be empty
  And the "Description" field should be empty
  And the "Product ID" field should be empty
  And the "Meta" field should be empty
  And the "Begin date" field should be empty
  And the "End date" field should be empty
  When I paste the "Promotion ID" field
  And I press the "Retrieve" button
  Then I should see message containing "retrieved successfully"
  And I should see "Cheese Burger Coupon" in the "Name" field
  And I should see "$5 off on your purchase of cheese burger" in the "Description" field
  And I should see "20" in the "Product ID" field
  And I should see "Active" in the "Status" dropdown
  And I should see "Coupon" in the "Type" dropdown
  And I should see "{"dollarsOff": 5}" in the "Meta" field
  And I should see "26-Nov-2021 (00:00:00.000000)" in the "Begin date" field
  And the "End date" field should be empty

Scenario: List all promotions
  When I visit the "Home Page"
  And I press the "Search" button
  Then I should be in search mode
  When I check the "Name" radio
  And I set the "Name" empty
  And I press the "Search" button
  Then I should see "Market Black Friday" in the results
  And I should see "Amazing Toaster Discount" in the results
  And I should see "MacBook Pro Discount" in the results
  And I should see "Grand Theft Auto Trilogy Coupon" in the results
  And I should see "Chips Ahoy" in the results

Scenario: Query promotions by Product ID
  When I visit the "Home Page"
  And I set the "Name" empty
  And I set the "Product ID" to "15"
  Then the "Name" field should be empty
  When I press the "Search" button
  Then I should be in search mode
  And I should see "Amazing Toaster Discount" in the results
  And I should not see "MacBook Pro Discount" in the results
  And I should not see "Market Black Friday" in the results
  And I should not see "Grand Theft Auto Trilogy Coupon" in the results
  And I should not see "Chips Ahoy" in the results

Scenario: Read a promotion
  When I visit the "Home Page"
  And I set the "Promotion ID" empty
  And I copy the #1 Promotion ID to the clipboard
  Then the "Promotion ID" field should be empty
  When I paste the "Promotion ID" field
  And I press the "Retrieve" button
  Then I should see message containing "retrieved successfully"
  And I should see "Market Black Friday" in the "Name" field
  And I should see "Amazing 20% discount on all purchases on Black Friday" in the "Description" field
  And the "Product ID" field should be empty
  And I should see "Active" in the "Status" dropdown
  And I should see "Percentage" in the "Type" dropdown
  And I should see "{"percentOff": 0.2}" in the "Meta" field
  And I should see "26-Nov-2021 (00:00:00.000000)" in the "Begin date" field
  And I should see "27-Nov-2021 (00:00:00.000000)" in the "End date" field

Scenario: Delete a promotion
  When I visit the "Home Page"
  And I set the "Promotion ID" empty
  And I copy the #1 Promotion ID to the clipboard
  Then the "Promotion ID" field should be empty
  When I paste the "Promotion ID" field
  And I press the "Retrieve" button
  Then I should see message containing "retrieved successfully"
  And I should see "Market Black Friday" in the "Name" field
  And I should see "Amazing 20% discount on all purchases on Black Friday" in the "Description" field
  And the "Product ID" field should be empty
  And I should see "Active" in the "Status" dropdown
  And I should see "Percentage" in the "Type" dropdown
  And I should see "{"percentOff": 0.2}" in the "Meta" field
  And I should see "26-Nov-2021 (00:00:00.000000)" in the "Begin date" field
  And I should see "27-Nov-2021 (00:00:00.000000)" in the "End date" field
  When I press the "Delete" button
  Then I should see message containing "deleted successfully"
  When  I paste the "Promotion ID" field
  And I press the "Retrieve" button
  Then I should see message containing "not found"

Scenario: Activate a Promotion
  When I visit the "Home Page"
  And I press the "Search" button
  Then I should be in search mode
  And I should see "Cheese Burger Coupon" in the results
  And I should see "MacBook Pro Discount" in the results
  And I should see "Grand Theft Auto Trilogy Coupon" in the results
  And I should see "Chips Ahoy" in the results
  When I select "Status" button
  And I select "Inactive" in the "Status" dropdown
  And I press the "Search" button
  Then I should see "Amazing Toaster Discount" in the results
  When I copy the Promotion ID to the clipboard
  And I visit the "Home Page"
  And I paste the "Promotion ID" field
  And I press the "Retrieve" button
  Then I should see message containing "retrieved successfully"
  When I press the "Activate" button
  Then I should see message containing "activated successfully"
  When I press the "Reset" button
  And I select "Active" in the "Status" dropdown
  And I press the "Search" button
  Then I should be in search mode
  And I should see "Cheese Burger Coupon" in the results
  And I should see "Amazing Toaster Discount" in the results
  And I should see "MacBook Pro Discount" in the results
  And I should see "Grand Theft Auto Trilogy Coupon" in the results
  And I should see "Chips Ahoy" in the results

Scenario: Deactivate a Promotion
  When I visit the "Home Page"
  And I select "Active" in the "Status" dropdown
  And I press the "Search" button
  Then I should be in search mode
  And I should see "Cheese Burger Coupon" in the results
  And I should see "Amazing Toaster Discount" in the results
  And I should see "MacBook Pro Discount" in the results
  And I should see "Grand Theft Auto Trilogy Coupon" in the results
  And I should see "Chips Ahoy" in the results
  When I copy the Promotion ID of "Amazing Toaster Discount" to the clipboard
  And I visit the "Home Page"
  And I paste the "Promotion ID" field
  And I press the "Retrieve" button
  Then I should see message containing "retrieved successfully"
  When I press the "Deactivate" button
  Then I should see message containing "deactivated successfully"
  When I press the "Reset" button
  And I select "Inactive" in the "Status" dropdown
  And I press the "Search" button
  Then I should be in search mode
  And I should see "Amazing Toaster Discount" in the results
