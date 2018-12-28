Feature: Helpers are just what they say they are -- they help!

  Scenario: Signature Generation
    Given I have an app_id of 123
    And I have a secret of s3cr3t
    And I have this content abcdefg
    When I generate a signature
    Then I expect the signature to be 'VILJCzdmbsVCYTx_QSl8HttAEmOSBjSW-de1ZQDaRooxb_3vK36Hm5VF5OWgJl6Qvb4c9Kby5vCkYo0mM6MOVw'
