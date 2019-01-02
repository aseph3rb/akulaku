Feature: Akulaku API Gateway

  Scenario: Base URL for Sandbox API
    Given a gateway with app id of 123, secret key of s3cret, sandbox is True
    When i check base url
    Then i get url "http://testmall.akulaku.com"

  Scenario: Base URL for Production API
    Given a gateway with app id of 123, secret key of s3cret, sandbox is False
    When i check base url
    Then i get url "https://mall.akulaku.com"

  Scenario: Generate AkuLaku Redirect URL for Sandbox
    Given a gateway with app id of 123, secret key of s3cret, sandbox is True
    And order number of 12345
    When i try to get akulaku url
    Then i get akulaku url "http://testmall.akulaku.com/v2/openPay.html?appId=123&refNo=12345&sign=uQ2RsMfl2sUy4yzP1Pbyko1DyP1OF7tRcUn_YydkKrPFgcOMflDCcnmyqD-qUKQddQWi8cmLXynZtrPV0HeXkA&lang=id"

 Scenario: Generate AkuLaku Redirect URL for Production
    Given a gateway with app id of 123, secret key of s3cret, sandbox is False
    And order number of 12345
    When i try to get akulaku url
    Then i get akulaku url "https://mall.akulaku.com/v2/openPay.html?appId=123&refNo=12345&sign=uQ2RsMfl2sUy4yzP1Pbyko1DyP1OF7tRcUn_YydkKrPFgcOMflDCcnmyqD-qUKQddQWi8cmLXynZtrPV0HeXkA&lang=id"

 Scenario: Send new order request to AkuLaku Production API
   Given a gateway with app id of 123, secret key of s3cret, sandbox is False
   And object OrderRequest
   When I make a successful new order request
   Then i get orderId response

 Scenario: Send new order request to AkuLaku Production API
   Given a gateway with app id of 123, secret key of s3cret, sandbox is False
   And object OrderRequest
   When I make a error response
   Then i get Akulaku Error
