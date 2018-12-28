Feature: Akulaku API Gateway

  Scenario: to get base url
    Given a gateway with app id of 123, secret key of s3cret, sandbox is True
    When i check base url
    Then i get url "http://testmall.akulaku.com"

  Scenario: to get base url
    Given a gateway with app id of 123, secret key of s3cret, sandbox is False
    When i check base url
    Then i get url "https://mall.akulaku.com"

  Scenario: get akulaku url to redirect to this URL
    Given a gateway with app id of 123, secret key of s3cret, sandbox is True
    And order number of 12345
    When i try to get akulaku url
    Then i get akulaku url "http://testmall.akulaku.com/v2/openPay.html?appId=123&refNo=12345&sign=uQ2RsMfl2sUy4yzP1Pbyko1DyP1OF7tRcUn_YydkKrPFgcOMflDCcnmyqD-qUKQddQWi8cmLXynZtrPV0HeXkA&lang=id"
