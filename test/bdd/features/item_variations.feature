Feature: Get, Create & Update Item Variations

  Background:
    Given a resource url called "/api/v1/items/1/variations/"

  Scenario: Add Item Variation
    Given I have the following data
      | item_id | option_id | stock_on_hand | unit_cost | re_order_level | re_order_quantity | is_active |
      | 1       | 1         | 100.00        | 10.00     | 100.00         | 100.00            | true      |
    When I save the data
    Then I get a "201" response
    And I get a field "status" containing "ok"
    And I get a field "message" containing "ok"

  Scenario: Update Item Variation
    Given I have a resource with the id "1"
    And I want to update its data to the following data
      | item_id | option_id | stock_on_hand | unit_cost | re_order_level | re_order_quantity | is_active |
      | 1       | 1         | 100.00        | 10.00     | 100.00         | 100.00            | true      |
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
      | url                           | status_code | status | message |
      | /                             | 200         | ok     | ok      |
      | /api/v1/items/                | 200         | ok     | ok      |
      | /api/v1/items/1/              | 200         | ok     | ok      |
      | /api/v1/items/1/variations/   | 200         | ok     | ok      |
      | /api/v1/items/1/variations/1/ | 200         | ok     | ok      |
