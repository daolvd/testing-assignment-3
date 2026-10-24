# Source: blackbox-test-cases.md, T003 - F11 User account management. Technique: Output Partitioning.
@F11 @T003
Feature: F11 - User account management
  Update personal details through Edit Account, and reject invalid values without changing the saved profile.
  Prerequisites that are unavailable must be reported as Blocked before execution.

  @T003-S1 @OP-F11-01 @valid
  Scenario: T003-S1 - Save valid personal details
    Given I am logged in with the dedicated test account
    When I click Edit Account and record PROFILE_BASELINE
    And I enter the following profile values:
      | Field      | Value      |
      | First Name | AlexM3     |
      | Telephone  | 0412345678 |
    Then only the entered fields should differ from PROFILE_BASELINE
    When I click Continue on the profile form
    Then My Account should open after the save

  @T003-S2 @OP-F11-02 @invalid
  Scenario: T003-S2 - Reject an empty Last Name
    Given I am logged in with the dedicated test account
    When I click Edit Account and record PROFILE_BASELINE
    And I enter the following profile values:
      | Field     | Value |
      | Last Name |       |
    Then only the entered fields should differ from PROFILE_BASELINE
    When I click Continue on the profile form
    Then the Edit Account form should remain open
    And the validation beside Last Name should identify it as invalid

  @T003-S3 @OP-F11-03 @invalid
  Scenario: T003-S3 - Reject a malformed email
    Given I am logged in with the dedicated test account
    When I click Edit Account and record PROFILE_BASELINE
    And I enter the following profile values:
      | Field  | Value            |
      | E-Mail | m3-invalid-email |
    Then only the entered fields should differ from PROFILE_BASELINE
    When I click Continue on the profile form
    Then Chrome should block submission at the E-Mail field
