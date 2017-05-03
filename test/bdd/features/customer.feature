Feature: Create, Update, Delete, Get Customer
  Scenario: Get Customer
    Given customer id '1' is in the system
    When I retrieve the customer id '1'
    Then I get the customer '200' response
    And the following customer details are shown:
    | id | first_name | last_name | address | city | state | postal_code | country | phone | email | user_id | billing_address | shipping_address | date_created |
    | 1 | first1 | last1 | address1 | city1 | state1 | postalcode1 | country1 | phone1 | test@estore.com | 1 | baddress1 | saddress1 | 2016-03-11 11:49:17 |


  Scenario: Get Customer not in the Database
    Given I access the customer url '/api/v1/customers/2/'
    When I retrieve the customer JSON result
    Then I get the customer '200' response
    And it should have a customer field 'status' containing 'ok'
    And it should have a customer field 'message' containing 'No entries found'
    And it should have a customer field 'count' containing '0'
    And it should have an empty customer field 'entries'


  Scenario: Create Customer
    Given I have the following data
    | id | first_name | last_name | address | city | state | postal_code | country | phone | email | user_id | billing_address | shipping_address | date_created |
    | 9 | first9 | last9 | address9 | city9 | state9 | postalcode9 | country9 | phone9 | test9@estore.com | 9 | baddress9 | saddress9 | 2016-03-11 11:49:17 |
    When I POST to the customer url '/api/v1/customers/'
    Then I get the create customer '201' response
    And I should get a customer field 'status' containing 'ok'
    And I should get a customer field 'message' containing 'ok'

  Scenario: Create Duplicate Customer
    Given I have the following data
    | id | first_name | last_name | address | city | state | postal_code | country | phone | email | user_id | billing_address | shipping_address | date_created |
    | 9 | first9 | last9 | address9 | city9 | state9 | postalcode9 | country9 | phone9 | test9@estore.com | 9 | baddress9 | saddress9 | 2016-03-11 11:49:17 |
    When I POST to the customer url '/api/v1/customers/'
    Then I get the create customer '201' response
    And I should get a customer field 'status' containing 'ok'
    And I should get a customer field 'message' containing 'CUSTOMER EXISTS'


  Scenario: Create Customer with Missing Details
    Given I have the following data
    | id | first_name | last_name | address | city | state | postal_code | country | phone | email | user_id | billing_address | shipping_address | date_created |
    | 10 |  | | address9 | city9 | state9 | | country9 | phone9 |  | 9 |  |  | 2016-03-11 11:49:17 |
    When I POST to the customer url '/api/v1/customers/'
    Then I get the create customer '201' response
    And I should get a customer field 'status' containing 'ok'
    And I should get a customer field 'message' containing 'error'