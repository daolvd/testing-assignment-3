# Source: blackbox-test-cases.md, Feature F3. Schedule: D3.
# Dependency: F1 -> F2 -> F3. Record the authorised account identifier, never its password.
@F3
Feature: F3 - Address Book
  Save valid addresses, reject incomplete addresses, and protect the default address.
  Prerequisites that are unavailable must be reported as Blocked before execution.

  @TC-F3-01 @OP-F3-1 @valid
  Scenario: TC-F3-01 - Save a complete address
    Given I am logged in to an authorised test account with an accessible Address Book
    And the test address is not already present
    When I open My Account Address Book and record the existing addresses and default address
    And I select New Address
    And I enter the following address:
      | Field          | Value            |
      | First Name     | Alex             |
      | Last Name      | Tester           |
      | Company        |                  |
      | Address 1      | 15 George Street |
      | Address 2      |                  |
      | City           | Sydney           |
      | Postcode       | 2000             |
      | Country        | Australia        |
      | Region / State | New South Wales  |
      | Default        | No               |
    And I submit the address using Continue
    Then a save-success confirmation should appear
    And the address list should contain exactly one new entry matching the entered address
    When I refresh Address Book and reopen the new address using Edit
    Then the saved address fields should match the entered address
    And the existing addresses and previously selected default address should remain unchanged
    # Cleanup: Delete the newly created nondefault address.

  @TC-F3-02 @OP-F3-2 @invalid
  Scenario: TC-F3-02 - Submit an address without a first name
    Given I am logged in to an authorised test account with an accessible Address Book
    When I open Address Book and record the existing addresses and default address
    And I select New Address
    And I enter the following address:
      | Field          | Value            |
      | First Name     |                  |
      | Last Name      | Tester           |
      | Company        |                  |
      | Address 1      | 15 George Street |
      | Address 2      |                  |
      | City           | Sydney           |
      | Postcode       | 2000             |
      | Country        | Australia        |
      | Region / State | New South Wales  |
      | Default        | No               |
    And I submit the address using Continue
    Then a visible validation error should identify First Name as invalid or required
    And no save-success confirmation should appear
    When I return to Address Book and refresh it
    Then the incomplete address should not be saved
    And the existing addresses and default address should remain unchanged
    # Cleanup: None expected; remove any accidentally saved test entry if a defect occurs.

  # A1 is unconfirmed in the source. Confirm it against assignment requirements
  # before execution; different behaviour is not a defect until A1 is confirmed.
  @TC-F3-03 @OP-F3-3 @edge_case @requires_A1
  Scenario: TC-F3-03 - Attempt to delete the default address
    Given acceptance assumption A1 that default-address deletion is prohibited has been confirmed
    And I am logged in to a disposable test account with exactly one address that is its default
    And I have recorded the complete default address and its default designation
    When I open Address Book and confirm the recorded address is present
    And I select Delete for the default address and confirm if prompted
    Then a warning should explain that the default address cannot be deleted
    And no deletion-success confirmation should appear
    When I refresh Address Book and reopen the recorded address if available
    Then the address should remain present with its original values and default designation
    # Cleanup: If deletion unexpectedly succeeds, restore the recorded address and default designation.
