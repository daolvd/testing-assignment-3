# Source: blackbox-test-cases.md, T002 - F7 Product Details. Technique: Output Partitioning.
@F7 @T002
Feature: F7 - Product Details
  A guest reaches a product through Search or the category menu and inspects its details.
  Prerequisites that are unavailable must be reported as Blocked before execution.

  @T002-S1 @OP-F7-01 @valid
  Scenario: T002-S1 - Find iPhone through Search and inspect its standard product details
    Given I am a guest on the Home page with US Dollar selected
    When I search for iPhone
    Then the search results should contain an iPhone card for product ID 40
    When I open the product card named iPhone
    Then the details page should show the heading iPhone for product ID 40
    And the product details should show:
      | Detail       | Value    |
      | Brand        | Apple    |
      | Availability | In Stock |
      | Price        | $123.20  |
      | Ex Tax       | $101.00  |
    When I open the main product image and close the image viewer
    Then the enlarged image should load and the viewer should close on the same product
    And the Description tab should show a non-empty description
    When I reload the product page
    Then the product information and image should be unchanged after the reload

  @T002-S2 @OP-F7-02 @edge
  Scenario: T002-S2 - Browse Laptops and inspect an out-of-stock product
    Given I am a guest on the Home page with US Dollar selected
    When I open the Laptops & Notebooks menu and click Show All Laptops & Notebooks
    Then the category listing should contain a MacBook Air card for product ID 44
    When I open the product card named MacBook Air
    Then the details page should show the heading MacBook Air for product ID 44
    And the product details should show:
      | Detail       | Value        |
      | Brand        | Apple        |
      | Availability | Out Of Stock |
      | Price        | $1,202.00    |
    And the main image should be loaded and the Description tab should be readable
    When I reload the product page
    Then the product information and image should be unchanged after the reload

  @T002-S3 @OP-F7-03 @invalid
  Scenario: T002-S3 - Open a product page for a product ID that does not exist
    Given I am a guest on the Home page with US Dollar selected
    When I open the product page for product ID 99999
    Then the page should state Product not found!
    And no product details should be shown
    When I click Continue on the not-found page
    Then the Home page should open
