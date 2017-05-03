Feature: Create, Get, Delete and Update Cart

#  Create sunny case
  Scenario: Create cart
    Given I have the following data
    |id | session_id | date_created| customer_id| is_active |
    |1  | 1          | 2016-03-15  | 1          | True      |
    When I Post the cart to resource_url  '/api/v1/carts/'
    Then I should have a status code '200'
    And I should get a status 'ok'
    And I should get a message 'OK'

#  Create rainy case
  Scenario: Create a duplicate cart
    Given I have the following data
    |id | session_id | date_created| customer_id| is_active |
    |1  | 1          | 2016-03-15  | 1          | True      |
    When I Post the cart to resource_url  '/api/v1/carts/'
    Then I should have a status code '200'
    And I should get a status 'ok'
    And I should get a message 'ID EXISTS'


#  Get sunny case
  Scenario: Get cart
    Given cart '1' is in the system
    When I retrieve the cart '1'
    Then I should have a status code '200'
    And the following cart details are returned :
      | session_id | date_created| customer_id| is_active |
      | 1          | 2016-03-15  | 1          | True      |


#  Get rainy case
  Scenario: Get a cart that doesn't exist
    Given I retrieve the cart '2'
    When i retrieve a JSON result
    Then I should have a status code '200'
    And I should get a status 'ok'
    And it should  have a field "message" 'No entries found'
    And it should  have a field "count" 0
    And it should  have an empty field " entries "

#  Scenario: Delete cart
#    Given I have the following cart details
#      |id | session_id | date_created| customer_id| is_active |
#      |1  | 1          | 2016-03-15  | 1          | True      |
#    When I Delete the cart '1' with source url 'api/v1/carts/1/'
#    Then I should get a '200' status code
#    And I should get a "status" containing "ok"
#    And I should get a "message" containing "ok"
#    And it should have an empty field " entries "