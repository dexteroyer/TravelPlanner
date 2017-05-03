Feature: Get, Create & Update Items

  Background:
    Given a resource url called "/api/v1/items/"

  Scenario: Add Item
    Given I have the following data
      | name | description | date_added     | date_updated   | is_active |
      | name | description | 2001-1-1 1:1:1 | 2001-1-1 1:1:1 | true      |
    When I save the data
    Then I get a "201" response
    And I get a field "status" containing "ok"
    And I get a field "message" containing "ok"

  Scenario: Update Item
    Given I have a resource with the id "1"
    And I want to update its data to the following data
      | name | description | date_added     | date_updated   | is_active |
      | name | description | 2001-1-1 1:1:1 | 2001-1-1 1:1:1 | true      |
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
      | url              | status_code | status | message |
      | /                | 200         | ok     | ok      |
      | /api/v1/items/   | 200         | ok     | ok      |
      | /api/v1/items/1/ | 200         | ok     | ok      |
