Feature: Get, Create & Update Wishlist Item

  Background:
    Given a resource url called "/api/v1/wishlists/1/items/"

  Scenario: Add Wishlist Item
    Given I have the following data
      | wishlist_item_id | wishlist_id | item_id | time_stamp  |
      | 1                | 1           | 1       | 1/1/1 1:1:1 |
    When I save the data
    Then I get a "201" response
    And I get a field "status" containing "ok"
    And I get a field "message" containing "ok"

  Scenario: Update Wishlist Item
    Given I have a resource with the id "1"
    And I want to update its data to the following data
      | wishlist_item_id | wishlist_id | item_id | time_stamp  |
      | 1                | 1           | 1       | 1/1/1 1:1:1 |
    When I update the data
    Then I get a "200" response
    And I get a field "status" containing "ok"
    And I get a field "message" containing "ok"

  Scenario Outline: Retrieve resource
    Given I access the url "<url>"
    Then I get a "<status_code>" response
    And I get an "<status>" status
    And I get an "<message>" message

    Examples:
      | url                          | status_code | status | message |
      | /                            | 200         | ok     | ok      |
      | /api/v1/wishlists/1/items/   | 200         | ok     | ok      |
      | /api/v1/wishlists/1/items/1/ | 200         | ok     | ok      |

Feature: Get and Create Wishlist Items


  Scenario: Create Wishlist Item - sunny case
    Given I have the details of wishlist items
    | wishlist_item_id | wishlist_id | item_id | time_stamp |
    | 2 | 1 | 3 | 2016-04-14 |
    When I POST to url '/api/v1/wishlist_items/' the wishlist items
    Then I should get status code response '200'
    And I should get 'ok' status
    And I should get 'OK' message


  Scenario: Create a duplicate wishlist item - rainy case
    Given I have the details of wishlist items
    | wishlist_item_id | wishlist_id | item_id | time_stamp |
    | 2 | 1 | 3 | 2016-04-14 |
    When I POST to url '/api/v1/wishlist_items/' the wishlist items
    Then I should get status code response '200'
    And I should get 'ok' status
    And I should get 'ERROR' message for duplication


  Scenario: Create an invalid wishlist item - rainy case
    Given I have the details of wishlist items
    | wishlist_item_id | wishlist_id | item_id | time_stamp |
    | d | x | t | r |
    When I POST to url '/api/v1/wishlist_items/' the wishlist items
    Then I should get status code response '200'
    And I should get 'error' status for invalid details
    
    
  Scenario: Create an incomplete wishlist - rainy case
    Given I have the details of wishlist items
    | wishlist_item_id | wishlist_id | item_id | time_stamp |
    |  | 1 |  | 2016-04-14 |
    When I POST to url '/api/v1/wishlist/' the wishlist
    Then I should get status code response '200'
    And I should get 'ok' status
    And I should get 'ERROR' message for incomplete details
 

  Scenario: Get Wishlist Item - sunny case
    Given wishlist item '2' is in the system
    When I retrieve the wishlist '2'
    Then I should have a status code response '200'
    And the following details are returned :
      | wishlist_item_id | wishlist_id | item_id | time_stamp |
      | 2 | 1 | 3 | 2016-04-14 |


  Scenario: Get a wishlist item that doesn't exist - rainy case
    Given I retrieve a wishlist item with id '4'
    When I retrieve the wishlist item JSON result
    Then I should have a status code response '200'
    And I should get the status says 'ok'
    And it should  have a field message saying 'No entries found'
    And it should  have a field count '0'
    And it should  have an empty field 'entries'

