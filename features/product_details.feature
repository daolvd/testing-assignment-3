# Source: blackbox-test-cases.md, Feature F7. Schedule: D4.
# Dependency: F4 -> F6 -> F7. Verify current catalogue data before execution.
@F7
Feature: F7 - Product Details
  Display existing products, unavailable products, and products with zero reviews.
  Prerequisites that are unavailable must be reported as Blocked before execution.

  @TC-F7-01 @OP-F7-1 @valid
  Scenario: TC-F7-01 - View an existing product
    Given the catalogue contains "iPhone" with product ID "40"
    And catalogue or search navigation is available
    When I locate iPhone through the catalogue or search flow and record its displayed name and price
    And I select the product to open Product Details
    Then the details page should identify iPhone and show its image, price, description, and availability
    And its displayed name and price should match the listing in the same currency and customer session
    When I refresh the product details page
    Then product ID "40" and its details should remain displayed
    And no product-not-found message should appear
    # Cleanup: None.

  @TC-F7-02 @OP-F7-2 @invalid
  Scenario: TC-F7-02 - Request a nonexistent product
    Given product ID "999999999" is confirmed absent or replaced with a recorded confirmed absent positive numeric ID
    When I open a known existing product page
    And I replace its product_id URL parameter with the confirmed absent ID and load the URL
    Then a clear unavailable or not-found state should appear instead of a purchasable product
    And no stale name, price, or purchase control should be presented as belonging to the absent ID
    And usable navigation back to the store should be available
    And no raw server error or stack trace should appear
    # Cleanup: None.

  @TC-F7-03 @OP-F7-3 @edge_case
  Scenario: TC-F7-03 - View a product with zero reviews
    Given product ID "40" has zero reviews or another confirmed zero-review product has its name and ID recorded
    When I open the selected product details page
    And I inspect its review count and rating summary
    And I open or scroll to its reviews area
    Then the product details should remain available with a review count of 0
    And the reviews area should show an empty state or no review entries without fabricated reviews
    And the rating should use the site empty-state presentation without NaN or division-by-zero errors
    And the review-entry control should remain available
    # Cleanup: None; do not submit a review.
