Feature: Get and Create Wishlist


  Scenario: Create Wishlist - sunny case
    Given I have the details of wishlist
    | wishlist_id | wishlist_name |
    | 1 | noob |
    When I POST to url '/api/v1/wishlist/' the wishlist
    Then I should get status code response '200'
    And I should get 'ok' status
    And I should get 'OK' message


  Scenario: Create a duplicate wishlist - rainy case
    Given I have the details of wishlist
    |wishlist_id | wishlist_name |
    | 1 | noob |
    When I POST to url '/api/v1/wishlist/' the wishlist
    Then I should get status code response '200'
    And I should get 'ok' status
    And I should get 'ERROR' message for duplication


  Scenario: Create an invalid wishlist - rainy case
    Given I have the details of wishlist
    |wishlist_id | wishlist_name |
    | noob | 1 |
    When I POST to url '/api/v1/wishlist/' the wishlist
    Then I should get status code response '200'
    And I should get 'error' status for invalid details
    
    
  Scenario: Create an incomplete wishlist - rainy case
    Given I have the details of wishlist
    |wishlist_id | wishlist_name |
    | 1 |  |
    When I POST to url '/api/v1/wishlist/' the wishlist
    Then I should get status code response '200'
    And I should get 'ok' status
    And I should get 'ERROR' message for incomplete details
 


  



  Scenario: Get Wishlist - sunny case
    Given wishlist '1' is in the system
    When I retrieve the wishlist '1'
    Then I should have a status code response '200'
    And the following details are returned :
      |wishlist_id | wishlist_name |
      | 1 | noob |


  Scenario: Get a wishlist that doesn't exist - rainy case
    Given I retrieve a wishlist with id '2'
    When I retrieve the wishlist JSON result
    Then I should have a status code response '200'
    And I should get the status says 'ok'
    And it should  have a field message saying 'No entries found'
    And it should  have a field count '0'
    And it should  have an empty field 'entries'


  
  

