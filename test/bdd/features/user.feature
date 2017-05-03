Feature: Handle storing and retrieving customer details

  Scenario: Get User
    Given user id '1' is in the system
    When I retrieve the user '1'
    Then I get the '200' response
    And the following user details are shown:
      | user_id | username | email            | password | date_created | is_admin |
      | 1       | user9    | user9@estore.com | user9    | 1/1/1 1:1:1  | true     |


  Scenario: Get User not in the Database
    Given I access the user id '2'
    When I retrieve the user JSON result
    Then I get the '200' response
    And it should have a user field 'status' containing 'ok'
    And it should have a user field 'message' containing 'No entries found'
    And it should have a user field 'count' containing '0'
    And it should have an empty field 'entries'


  Scenario: Create User
    Given I have the following user details:
      | user_id | username | email            | password | date_created | is_admin |
      | 1       | user9    | user9@estore.com | user9    | 1/1/1 1:1:1  | true     |
    When I POST to the user url '/api/v1/users/'
    Then I get the create '201' response
    And I should get a user field 'status' containing 'ok'
    And I should get a user field 'message' containing 'OK'


  Scenario: Create Duplicate User
    Given I have the following user details:
      | user_id | username | email            | password | date_created | is_admin |
      | 1       | user9    | user9@estore.com | user9    | 1/1/1 1:1:1  | true     |
    When I POST to the user url '/api/v1/users/'
    Then I get the create '201' response
    And I should get a user field 'status' containing 'ok'
    And I should get a user field 'message' containing 'USER EXISTS'


  Scenario: Create User with missing Details
    Given I have the following user details:
      | user_id | username | email            | password | date_created | is_admin |
      | 1       | | user9@estore.com | user9    | 1/1/1 1:1:1  | true     |
    When I POST to the user url '/api/v1/users/'
    Then I get the create '201' response
    And I should get a user field 'status' containing 'ok'
    And I should get a user field 'message' containing 'error'