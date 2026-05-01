# We will be testing following unit cases -
#   1. read_customer_df = 12435
#   2. read_orders_df = 68883
#   3. filter_closed_orders = 7556
#   4. read_app_config
#   5. count_orders_state

import pytest
from lib.DataReader import read_customers,read_orders
from lib.DataManipulation import filter_closed_orders, count_orders_state, filter_orders_generic
from lib.ConfigReader import get_app_config

@pytest.mark.skip()
def test_read_customers_df(spark):
    customers_count = read_customers(spark,'LOCAL').count()
    assert customers_count == 12435

@pytest.mark.skip()
def test_read_orders_df(spark):
    orders_count = read_orders(spark,'LOCAL').count()
    assert orders_count == 68884

@pytest.mark.skip()
def test_filter_closed_orders_df(spark):
    orders_df = read_orders(spark,'LOCAL')
    filtered_orders_count = filter_closed_orders(orders_df).count()
    assert filtered_orders_count == 7556

@pytest.mark.skip("Work in Progress")
def test_read_app_config():
    config = get_app_config('LOCAL')
    assert config["customers.file.path"] == "data/customers.csv"
    assert config["orders.file.path"] == "data/orders.csv"

@pytest.mark.skip()
def test_count_cust_state(spark, expected_result):
    customers_df = read_customers(spark,'LOCAL')
    actual_result = count_orders_state(customers_df)
    assert actual_result.collect() == expected_result.collect()

@pytest.mark.skip()
def test_check_closed_count(spark):
    orders_df = read_orders(spark,'LOCAL')
    count_orders = filter_orders_generic(orders_df,'CLOSED').count()
    assert count_orders == 7556

@pytest.mark.skip()
def test_check_pending_count(spark):
    orders_df = read_orders(spark,'LOCAL')
    count_orders = filter_orders_generic(orders_df,'PENDING_PAYMENT').count()
    assert count_orders == 15030

@pytest.mark.skip()
def test_check_complete_count(spark):
    orders_df = read_orders(spark,'LOCAL')
    count_orders = filter_orders_generic(orders_df,'COMPLETE').count()
    assert count_orders == 22900

@pytest.mark.transformation()
@pytest.mark.parametrize("status,count",[("CLOSED",7556),("PENDING_PAYMENT",15030),("COMPLETE",22900)])
def test_check_generic_count(spark,status,count):
    orders_df = read_orders(spark,'LOCAL')
    count_orders = filter_orders_generic(orders_df,status).count()
    assert count_orders == count