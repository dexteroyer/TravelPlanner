Feature: Get, Create & Update Item Attributes

  Background:
    Given a resource url called "/api/v1/items/1/attributes/"

  Scenario: Add Item Attribute
    Given I have the following data
      | attribute_id | item_id | attribute_value |
      | 1            | 1       | Default         |
    When I save the data
    Then I get a "201" response
    And I get a field "status" containing "ok"
    And I get a field "message" containing "ok"

  Scenario: Update Item Attribute
    Given I have a resource with the id "1"
    And I want to update its data to the following data
      | attribute_id | item_id | attribute_value |
      | 1            | 1       | New Default     |
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
      | /api/v1/items/1/attributes/   | 200         | ok     | ok      |
      | /api/v1/items/1/attributes/1/ | 200         | ok     | ok      |