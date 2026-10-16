# Source: blackbox-test-cases.md, Feature F11. Schedule: D6.
# Dependency: F10 -> F11. Prepare each case independently in an isolated session.
@F11
Feature: F11 - Update / Remove Cart
  Update valid quantities, reject nonnumeric quantities, and remove the last item.
  Prerequisites that are unavailable must be reported as Blocked before execution.

  Background:
    Given I have an isolated cart session with one currency, no coupon or voucher, and no selected shipping service
    And I have added one unit of an available product with no required options, no quantity discount at 2 units, and stock for 2 units
    And I use iPhone product ID "40" if it meets these fixture conditions
    And the cart contains exactly one product line with quantity 1
    And I have recorded the displayed unit price as U and any tax or fee rows using displayed currency precision

  @TC-F11-01 @OP-F11-1 @valid
  Scenario: TC-F11-01 - Update cart quantity
    When I open Shopping Cart and record the product, unit price, quantity, and totals
    And I change the quantity from 1 to 2 and select the line Update control
    Then the same single product line should show quantity 2 without a duplicate line
    And the line total should equal 2 times U
    And the subtotal should equal the sum of displayed line totals
    And the grand total should reconcile with the subtotal and displayed tax, fee, and discount rows
    When I refresh Shopping Cart
    Then quantity 2 and the recalculated totals should persist
    # Cleanup: Remove the test product.

  # A2 is unconfirmed in the source. Confirm it before execution. If the documented
  # behaviour is normalization or removal, the oracle must be resolved before testing.
  @TC-F11-02 @OP-F11-2 @invalid @requires_A2
  Scenario: TC-F11-02 - Submit a nonnumeric cart quantity
    Given acceptance assumption A2 that invalid quantity is rejected without removing the item or changing its valid quantity has been confirmed
    When I open Shopping Cart and record its original product, quantity, and totals
    And I attempt to replace quantity 1 with "abc"
    And I select Update if the field accepts the characters or record the visible input restriction
    Then the field should prevent nonnumeric entry or a visible validation response should reject the submitted value
    When I refresh Shopping Cart
    Then the original product should remain at quantity 1 with its original line total, subtotal, and grand total
    And no invalid numeric values or server errors should appear
    # Cleanup: Remove the test product; recreate the fixture if needed before another case.

  @TC-F11-03 @OP-F11-3 @edge_case
  Scenario: TC-F11-03 - Remove the last cart item
    When I open Shopping Cart and confirm there is exactly one product line
    And I select its Remove control and confirm if prompted
    Then the removed product line should disappear and an empty-cart message should appear
    And the header cart summary should show zero items and zero cart value in the selected currency
    And no stale product totals should remain
    When I refresh Shopping Cart and reopen the cart summary
    Then the empty-cart state and zero header cart summary should persist
    # Cleanup: None; the cart should be empty.
