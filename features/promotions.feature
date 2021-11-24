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
