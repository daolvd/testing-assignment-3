# Source: blackbox-test-cases.md, T001 - F3 Address Book. Technique: Input Partitioning.
@F3 @T001
Feature: F3 - Address Book
  Save a valid address, and reject an address with First Name or City empty.
  Prerequisites that are unavailable must be reported as Blocked before execution.

  @T001-S1 @IP-F3-01 @valid
  Scenario: T001-S1 - Save a valid address and verify it after a new login
    Given I am logged in with the dedicated test account
    And the default baseline address exists
    When I click Address Book on My Account and record the existing addresses
    Then the baseline should be present and no address should contain the scenario marker
    When I click New Address
    And I enter the following address:
      | Field          | Value                            |
      | First Name     | Alex                             |
      | Last Name      | Nguyen                           |
      | Company        |                                  |
      | Address 1      | 12 Harbour Street M3-RUN-T001S1  |
      | Address 2      |                                  |
      | City           | Sydney                           |
      | Postcode       | 2000                             |
      | Country        | Australia                        |
      | Region / State | New South Wales                  |
      | Default        | No                               |
    And I click Continue on the address form
    Then the address list should open without validation errors


  @T001-S2 @IP-F3-02 @invalid
  Scenario: T001-S2 - Reject an address with First Name empty and verify no record is saved
    Given I am logged in with the dedicated test account
    And the default baseline address exists
    When I click Address Book on My Account and record the existing addresses
    Then the baseline should be present and no address should contain the scenario marker
    When I click New Address
    And I enter the following address:
      | Field          | Value                            |
      | First Name     |                                  |
      | Last Name      | Nguyen                           |
      | Company        |                                  |
      | Address 1      | 12 Harbour Street M3-RUN-T001S2  |
      | Address 2      |                                  |
      | City           | Sydney                           |
      | Postcode       | 2000                             |
      | Country        | Australia                        |
      | Region / State | New South Wales                  |
      | Default        | No                               |
    And I click Continue on the address form
    Then the Add Address form should remain open
    And the validation beside First Name should identify it as invalid
  

  @T001-S3 @IP-F3-03 @invalid
  Scenario: T001-S3 - Reject an address with City empty and verify no record is saved
    Given I am logged in with the dedicated test account
    And the default baseline address exists
    When I click Address Book on My Account and record the existing addresses
    Then the baseline should be present and no address should contain the scenario marker
    When I click New Address
    And I enter the following address:
      | Field          | Value                            |
      | First Name     | Alex                             |
      | Last Name      | Nguyen                           |
      | Company        |                                  |
      | Address 1      | 12 Harbour Street M3-RUN-T001S3  |
      | Address 2      |                                  |
      | City           |                                  |
      | Postcode       | 2000                             |
      | Country        | Australia                        |
      | Region / State | New South Wales                  |
      | Default        | No                               |
    And I click Continue on the address form
    Then the Add Address form should remain open
    And the validation beside City should identify it as invalid

