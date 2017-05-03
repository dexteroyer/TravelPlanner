Feature: Get, Create & Update Images

  Background:
    Given a resource url called "/api/v1/items/1/images/"

  Scenario: Add Image
    Given I have the following data
      | item_id | image_url  | caption |
      | 1       | google.com | hi      |
    When I save the data
    Then I get a "201" response
    And I get a field "status" containing "ok"
    And I get a field "message" containing "ok"

  Scenario: Update Image
    Given I have a resource with the id "1"
    And I want to update its data to the following data
      | image_id | item_id | image_url  | caption |
      | 1        | 1       | google.com | hi      |
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
      | url                       | status_code | status | message |
      | /                         | 200         | ok     | ok      |
      | /api/v1/items/1/images/   | 200         | ok     | ok      |
      | /api/v1/items/1/images/1/ | 200         | ok     | ok      |
