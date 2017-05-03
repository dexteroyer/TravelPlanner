Feature: Create Get and Delete Cart Item

#  Create Sunny Case
   Scenario: Create Cart Item
      Given I have the following data
      | id | cart_id | product_id | quantity   | time_stamp         |
      | 1  | 1       | 1          | 1          | 2016-03-15 11:49:17|
      When I Post the cart item to resource_url  '/api/v1/carts/1/items/'
      Then I should get response '200'
      And I should get "status" 'ok'
      And I should get "message" 'OK'

#  Create Rainy Case
   Scenario: Create duplicate cart item
     Given I have the following data
     | id | cart_id | product_id | quantity   | time_stamp         |
     | 1  | 1       | 1          | 1          | 2016-03-15 11:49:17|
     When I Post the cart item to resource_url  '/api/v1/carts/1/items/'
     Then I should get response '200'
     And I should get "status" 'ok'
     And I should get "message" 'ID EXISTS'

# Sunny Case
  Scenario: Get cart item
    Given cart item '1' is in the system
    When I retrieve the cart item '1'
    Then I should get response '200'
    And the following cart item details are returned:
      | cart_id | product_id | quantity   | time_stamp         |
      | 1       | 1          | 1          | 2016-03-15 11:49:17|


#  """ Rainy Case """
  Scenario: Get a cart item that doesn't exist
    Given I retrieve the cart item '2'
    When i retrieve JSON result
    Then I should get response '200'
    And I should get "status" 'ok'
    And I should get a message containing 'No entries found'
    And it should have a field "count" 0
    And it should have an empty field " entries "


#  Scenario: Delete cart item
#    Given I have the following cart item details
#    | id | cart_id | product_id | quantity   | time_stamp         |
#    | 1  | 1       | 1          | 1          | 2016-03-15 11:49:17|
#    When I Delete the cart '1' with source url 'api/v1/cart_items/1/'
#    Then I should get a '200' status code
#    And I should get a "status" containing "ok"
#    And I should get a "message" containing "ok"
#    And it should have an empty field " entries "
