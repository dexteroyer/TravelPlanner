Feature: Create and Get Order

#  Create Sunny Case
  Scenario: Create order
    Given I have the following data
    |id| customer_id | payment_id | transaction_date | shipping_date | time_stamp          | transaction_status | total |
    |1 | 1           | 1          | 2016-03-11       | 2016-03-11    | 2016-03-11 11:49:17 | Pending            | 100.0 |
    When I Post the order to resource_url  '/api/v1/orders/'
    Then I should get a status of '200'
    And I should get a "status" 'ok'
    And I should get a "message" 'OK'

#  Create Rainy Case 2
  Scenario: Create a duplicate order
    Given I have the following data
     |id| customer_id | payment_id | transaction_date | shipping_date | time_stamp          | transaction_status | total |
     |1 | 1           | 1          | 2016-03-11       | 2016-03-11    | 2016-03-11 11:49:17 | Pending            | 100.0 |
    When I Post the order to resource_url  '/api/v1/orders/'
    Then I should get a status of '200'
    And I should get a "status" 'ok'
    And I should get a "message" 'ID EXISTS'

#  Create Rainy Case 2
  Scenario: Create an order with incomplete details
    Given I have the following data
     |id| customer_id | payment_id | transaction_date | shipping_date | time_stamp          | transaction_status | total |
     | 2 | 2           | 2          | 2016-03-11       | 2016-03-11    | 2016-03-11 11:49:17 | | 100.0 |
    When I Post the order to resource_url  '/api/v1/orders/'
    Then I should get a status of '200'
    And I should get a "status" 'ok'
    And I should get a "message" 'error'

#  Get Sunny Case
  Scenario: Get Order
    Given Order id '1' is in the system
    When I retrieve the order '1'
    Then I should get a status of '200'
    And the following orders are returned:
    | customer_id | payment_id | transaction_date | shipping_date | time_stamp          | transaction_status | total |
    | 1           | 1          | 2016-03-11       | 2016-03-11    | 2016-03-11 11:49:17 | Pending            | 100.0 |


#  Get Order Rainy Case
  Scenario: Get an order that doesn't exist
    Given I retrieve the order '2'
    When I retrieve a  JSON result
    Then I should get a status of '200'
    And I should get a "status" 'ok'
    And It should  have a "message" "No entries found"
    And It should  have a field "count" 0
    And It should  have an empty field " entries "
