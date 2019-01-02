# Created by fuad at 02/01/19
Feature: #Enter feature name here
  # Enter feature description here

  Scenario: OrderDetail serialization
    Given an OrderDetail with sku = 123, name = product_abc, unit_price = 10000, quantity = 3
    When I serialize the object
    Then the OrderDetail is serialized correctly

  Scenario: NewOrderRequest serialization
    Given a create order request
    When I serialize the object
    Then the order request is converted to a dictionary properly
