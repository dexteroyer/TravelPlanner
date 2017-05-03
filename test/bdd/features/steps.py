import json
from lettuce import *
from nose.tools import assert_equals
from app import create_app


@before.all
def before_all():
    world.app = create_app('testing')
    world.browser = world.app.test_client()


@step('a resource url called "(.*)"')
def given_a_resource_url(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.resource = url


# ----------------------------------------------------------------
# Common steps for retrieving data in any of the tables. We want to check its status, and fields.
@step('I access the url "(?P<url>.+)"')
def given_i_access_the_url_url(step, url):
    world.response = world.browser.get(url)
    world.response_data = json.loads(world.response.data)


@step('I get a "(?P<status_code>.+)" response')
def i_get_a_response(step, status_code):
    assert_equals(world.response.status_code, int(status_code))


@step('I get an "(?P<status>.+)" status')
def i_get_a_status(step, status):
    assert_equals(world.response_data['status'], status)


@step('I get an "(?P<message>.+)" message')
def i_get_a_message(step, message):
    assert_equals(world.response_data['message'], message)


# ----------------------------------------------------------------
# Common steps for adding data in any of the tables. We want to check its status, and fields.
@step("I have the following data")
def given_i_have_the_following_data(step):
    world.data = step.hashes[0]


@step('I save the data')
def i_post_to_the_url_url(step):
    world.response = world.browser.post(world.resource, data=json.dumps(world.data))
    print world.response
    world.response_data = json.loads(world.response.data)


@step('I get a field "(.*)" containing "(.*)"')
def i_get_a_field_field_containing_value(step, field, field_value):
    print world.response_data
    assert_equals(world.response_data[field], field_value)


# ----------------------------------------------------------------
# Common steps for updating data in any of the tables.


@step('I have a resource with the id "(.*)"')
def i_have_a_resource_with_id_id(step, id):
    world.resource_id = id


@step("I want to update its data to the following data")
def i_want_to_update_its_data(step):
    world.new_data = step.hashes[0]


@step("I update the data")
def i_send_a_put_request_from_client(step):
    url = world.resource + world.resource_id + "/"
    world.response = world.browser.put(url, data=json.dumps(world.new_data))
    world.response_data = json.loads(world.response.data)


# ----------------------------------------------------------------
# Create Supplier - Sunny & Rainy


@step("I Post the supplier to resource_url  \'(.*)\'")
def when_I_post_the_supplier_to_resource_url(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.supplier_post_uri = url
    world.supplier_post_response = world.browser.post(world.supplier_post_uri, data=json.dumps(world.data))


@step("I should get a response \'(.*)\'")
def then_i_should_get_a_201_response(step, expected_status_code):
    """
    :param expected_status_code:
    :type step: lettuce.core.Step
    """
    assert_equals(world.supplier_post_response.status_code, int(expected_status_code))


@step('I should get a "status" containing \'(.*)\'')
def and_i_should_get_a_status_containing_ok(step, status):
    """
    :type step: lettuce.core.Step
    """
    world.supplier_post_response_json = json.loads(world.supplier_post_response.data)
    print world.supplier_post_response_json
    assert_equals(world.supplier_post_response_json['status'], status)


@step('I should get a "message" containing \'(.*)\'')
def and_i_should_get_a_message_containing_ok(step, message):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.supplier_post_response_json['message'], message)


# ----------------------------------------------------------------
# Get Supplier

@step("supplier \'(.*)\' is in the system")
def given_supplier1_is_in_the_system(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.supplier = world.browser.get('/api/v1/suppliers/{}/'.format(id))
    world.resp = json.loads(world.supplier.data)
    assert_equals(world.resp['status'], 'ok')


@step("I retrieve the supplier \'(.*)\'")
def when_I_retrieve_the_supplier1(step, id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/suppliers/{}/'.format(id))


@step("the following supplier details are returned:")
def and_the_following_supplier_details(step):
    """
    :type step: lettuce.core.Step
    """
    resp = json.loads(world.response.data)
    assert_equals(world.resp['entries'], resp['entries'])


# ----------------------------------------------------------------
# Get Supplier

@step("I get the JSON result")
def when_I_get_the_JSON_result(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.response


@step('It should have a field "message" \'(.*)\'')
def and_it_should_have_a_field_message_ok(step, message):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    print world.resp
    assert_equals(world.resp['message'], message)


@step('It should have a field "count" 0')
def and_it_should_have_a_field_count0(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.resp['count'], '0')


@step('It should have an empty field "entries"')
def and_it_should_have_an_empty_field_entries(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp['entries']), 0)


@step("I Post the cart item to resource_url  \'(.*)\'")
def when_I_Post_the_cart_item_to_resource_url(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.cartItem_post_uri = url
    world.cartItem_post_response = world.browser.post(world.cartItem_post_uri, data=json.dumps(world.data))
    # world.response_data = json.loads(world.cartItem_post_response)


@step("I should get response \'(.*)\'")
def then_I_should_get_response(step, expected_status_code):
    """
    :param expected_status_code:
    :type step: lettuce.core.Step
    """
    assert_equals(world.cartItem_post_response.status_code, int(expected_status_code))


@step('I should get "status" \'(.*)\'')
def and_I_should_get_status(step, status):
    """
    :type step: lettuce.core.Step
    """
    world.cartItem_post_response_json = json.loads(world.cartItem_post_response.data)
    assert_equals(world.cartItem_post_response_json['status'], status)


@step('I should get "message" \'(.*)\'')
def and_I_should_get_message(step, message):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.cartItem_post_response_json['message'], message)


# ---------------------------------------------------------------------------
# Get Cart Item sunny case


@step("cart item \'(.*)\' is in the system")
def given_cart_item1_is_in_the_system(step, id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.cart_item = world.browser.get('/api/v1/carts/1/items/{}/'.format(id))
    world.resp = json.loads(world.cart_item.data)
    assert_equals(world.resp['status'], 'ok')


@step("I retrieve the cart item \'(.*)\'")
def when_I_retrieve_the_cart_item1(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/carts/1/items/{}/'.format(id))


@step("the following cart item details are returned:")
def then_the_following_cart_item_details_are_returned(step):
    """
    :type step: lettuce.core.Step
    """
    resp = json.loads(world.response.data)
    assert_equals(world.resp['entries'], resp['entries'])


# ---------------------------------------------------------------------------------
# Get Cart Item rainy case


@step("i retrieve JSON result")
def when_i_retrieve_JSON_result(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.response


@step('it should have a field "count" 0')
def and_it_should_have_an_empty_field_count0(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.resp['count'], '0')


@step('it should have an empty field " entries "')
def and_it_should_have_an_empty_field_entries(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp['entries']), 0)


@step('I should get a message containing \'(.*)\'')
def and_it_should_get_a_message_No_entries_found(step, message):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp['message'], message)


# -----------------------------------------------------------------------------
#  Create Cart sunny case and rainy case


@step("I Post the cart to resource_url  '/api/v1/carts/'")
def when_I_Post_the_cart_to_resource_url(step):
    """
    :type step: lettuce.core.Step
    """
    world.cart_post_uri = '/api/v1/carts/'
    world.cart_post_response = world.browser.post(world.cart_post_uri, data=json.dumps(world.data))


@step("I should have a status code \'(.*)\'")
def then_I_should_have_a_status_code(step, expected_status_code):
    """
    :param expected_status_code:
    :type step: lettuce.core.Step
    """
    assert_equals(world.cart_post_response.status_code, int(expected_status_code))


@step("I should get a status \'(.*)\'")
def and_I_should_get_a_status_ok(step, status):
    """
    :type step: lettuce.core.Step
    """
    world.cart_post_response_json = json.loads(world.cart_post_response.data)
    assert_equals(world.cart_post_response_json['status'], status)


@step("I should get a message \'(.*)\'")
def and_I_should_get_a_message_ok(step, message):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.cart_post_response_json['message'], message)


# ---------------------------------------------------------------------------------
#  Get Cart sunny case


@step("cart \'(.*)\' is in the system")
def given_cart_is_in_the_system(step, id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.cart = world.browser.get('/api/v1/carts/{}/'.format(id))
    world.resp = json.loads(world.cart.data)
    assert_equals(world.resp['status'], 'ok')


@step("I retrieve the cart \'(.*)\'")
def when_I_retrieve_the_cart(step, id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/carts/{}/'.format(id))


@step("the following cart details are returned :")
def and_the_following_details_are_returned(step):
    """
    :type step: lettuce.core.Step
    """
    resp = json.loads(world.response.data)
    assert_equals(world.resp['entries'], resp['entries'])


# ------------------------------------------------------------------------------------
# Get Cart rainy case


@step("i retrieve a JSON result")
def when_i_retrieve_a_JSON_result(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.response


@step('it should  have a field "count" 0')
def and_it_should_have_a_field_count0(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.resp['count'], '0')


@step('it should  have a field "message" \'(.*)\'')
def and_it_should_have_a_field_message_no_entries(step, message):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp['message'], message)


@step('it should  have an empty field " entries "')
def and_it_should_have_an_empty_field_entries(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp['entries']), 0)


# --------------------------------------------------------------------------------------------
# Create new order sunny case and rainy case


@step("I Post the order to resource_url  \'(.*)\'")
def when_I_Post_the_order_to_resource_url(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.order_post_uri = url
    world.order_response = world.browser.post(world.order_post_uri, data=json.dumps(world.data))


@step("I should get a status of \'(.*)\'")
def then_I_should_get_a_status_of(step, expected_status_code):
    """
    :param expected_status_code:
    :type step: lettuce.core.Step
    """
    assert_equals(world.order_response.status_code, int(expected_status_code))


@step('I should get a "status" \'(.*)\'')
def and_I_should_get_a_status(step, status):
    """
    :type step: lettuce.core.Step
    """
    world.order_response_json = json.loads(world.order_response.data)
    print world.order_response_json
    assert_equals(world.order_response_json['status'], status)


@step('I should get a "message" \'(.*)\'')
def and_I_should_get_a_message(step, message):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.order_response.data)
    assert_equals(world.resp['message'], message)


# -----------------------------------------------------------------------------------
# Get Order ID sunny case


@step("Order id \'(.*)\' is in the system")
def given_order_id1_is_in_the_system(step, id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.order = world.browser.get('/api/v1/orders/{}/'.format(id))
    world.resp = json.loads(world.order.data)
    assert_equals(world.resp['status'], 'ok')


@step("I retrieve the order \'(.*)\'")
def when_I_retrieve_the_order(step, id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/orders/{}/'.format(id))


@step("the following orders are returned:")
def and_the_following_orders_are_returned(step):
    """
    :type step: lettuce.core.Step
    """
    resp = json.loads(world.response.data)
    assert_equals(world.resp['entries'], resp['entries'])


# --------------------------------------------------------------------------------------
# Get order ID rainy case


@step("I retrieve a  JSON result")
def when_I_retrieve_a_JSON_result(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.response


@step('It should  have a "message" "No entries found"')
def and_It_should_have_a_message_No_entries_found(step):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp['message'], 'No entries found')


@step('It should  have a field "count" 0')
def and_It_should_have_a_field_count0(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.resp['count'], '0')


@step('It should  have an empty field " entries "')
def and_It_should_have_an_empty_field_entries(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp['entries']), 0)


# -----------------------------------------------------------------------------------
# Create order item sunny and rainy case


@step("I Post the order item to resource_url  \'(.*)\'")
def when_I_Post_the_order_item_to_resource_url(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.orderItem_post_uri = url
    world.orderItem_post_response = world.browser.post(world.orderItem_post_uri, data=json.dumps(world.data))


@step("I should have a response \'(.*)\'")
def then_I_should_have_a_status(step, expected_status_code):
    """
    :param expected_status_code:
    :type step: lettuce.core.Step
    """
    assert_equals(world.orderItem_post_response.status_code, int(expected_status_code))


@step('I should have a "status" containing \'(.*)\'')
def and_I_should_have_a_status_containing_ok(step, status):
    """
    :type step: lettuce.core.Step
    """
    world.orderItem_post_response_json = json.loads(world.orderItem_post_response.data)
    print world.orderItem_post_response_json
    assert_equals(world.orderItem_post_response_json['status'], status)


@step('I should have a "message" containing \'(.*)\'')
def and_I_should_have_a_message_containing_ok(step, message):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.orderItem_post_response_json['message'], message)


# ----------------------------------------------------------------------------------------------
# Get order item sunny case


@step("order item id \'(.*)\' is in the system")
def given_order_item_id1_is_in_the_system(step, id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.orderItem = world.browser.get('/api/v1/orders/1/items/{}/'.format(id))
    world.resp = json.loads(world.orderItem.data)
    assert_equals(world.resp['status'], 'ok')


@step("I retrieve the order item \'(.*)\'")
def when_I_retrieve_the_order_item(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/orders/1/items/{}/'.format(id))


@step("the following order item details are returned:")
def and_the_following_order_item_details_are_returned(step):
    """
    :type step: lettuce.core.Step
    """
    resp = json.loads(world.response.data)
    assert_equals(world.resp['entries'], resp['entries'])


# ------------------------------------------------------------------------------------------------
# Get order item rainy case


@step("I retrieve JSON result")
def when_I_retrieve_JSON_result(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.response


@step('It should have a field "count " 0')
def and_It_should_have_a_field_count0(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.resp['count'], '0')


@step('It should have an empty field " entries "')
def and_It_should_have_an_empty_field_entries(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp['entries']), 0)


@step('It should have a field "message " \'(.*)\'')
def and_It_should_have_a_field_message_No_entries_found(step, message):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp['message'], message)


# ------------------------------------------------------------------------
# customer

@step("customer id \'(.*)\' is in the system")
def step_impl(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.customer = world.browser.get('/api/v1/customers/{}/'.format(id))
    world.resp = json.loads(world.customer.data)
    assert_equals(world.resp['status'], 'ok')


@step("I retrieve the customer id \'(.*)\'")
def step_impl(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/customers/{}/'.format(id))


@step("I get the customer \'(.*)\' response")
def then_i_get_a_200_response(step, exp_status_code):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.response.status_code, int(exp_status_code))


@step("the following customer details are shown:")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    resp = json.loads(world.response.data)
    assert_equals(world.resp, resp)


@step("I access the customer url \'(.*)\'")
def step_impl(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.customer_uri = url


@step("I retrieve the customer JSON result")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get(world.customer_uri)


@step("it should have a customer field \'(.*)\' containing \'(.*)\'")
def step_impl(step, status, txt):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp[status], txt)


@step("it should have an empty customer field \'(.*)\'")
def step_impl(step, entries):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp[entries]), 0)


@step("I POST to the customer url \'(.*)\'")
def step_impl(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.customer_post_uri = url
    world.customer_post_response = world.browser.post(world.customer_post_uri, data=json.dumps(world.data))


@step("I get the create customer \'(.*)\' response")
def step_impl(step, exp_status_code):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.customer_post_response.status_code, int(exp_status_code))


@step("I should get a customer field \'(.*)\' containing \'(.*)\'")
def step_impl(step, status, txt):
    """
    :type step: lettuce.core.Step
    """
    world.customer_post_response_json = json.loads(world.customer_post_response.data)
    assert_equals(world.customer_post_response_json[status], txt)


# -------------------------
# User

@step("user id \'(.*)\' is in the system")
def given_user_id_1_is_in_the_system(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.user = world.browser.get('/api/v1/users/{}/'.format(id))
    world.resp = json.loads(world.user.data)
    assert_equals(world.resp['status'], 'ok')


@step("I retrieve the user \'(.*)\'")
def step_impl(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/users/{}/'.format(id))


@step("I get the \'(.*)\' response")
def then_i_get_a_200_response(step, exp_status_code):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.response.status_code, int(exp_status_code))


@step("the following user details are shown:")
def and_the_following_user_details_are_returned(step):
    """
    :param step:
    """
    resp = json.loads(world.response.data)
    assert_equals(world.resp, resp)


"""
Get User Rainy Case
"""


@step("I access the user id \'(.*)\'")
def step_impl(step, id):
    """
    :type step: lettuce.core.Step
    """
    world.user_uri = '/api/v1/users/2/'


@step("I retrieve the user JSON result")
def when_i_retrieve_the_json_results(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get(world.user_uri)


@step("it should have a user field \'(.*)\' containing \'(.*)\'")
def step_impl(step, status, txt):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp[status], txt)


@step("it should have an empty field \'(.*)\'")
def step_impl(step, entries):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp[entries]), 0)


""" CREATE USER """


@step("I have the following user details:")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    world.user1 = step.hashes[0]


@step("I POST to the user url \'(.*)\'")
def step_impl(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.user_post_uri = url
    print world.user_post_uri
    world.user_post_response = world.browser.post(world.user_post_uri, data=json.dumps(world.user1))


@step("I get the create \'(.*)\' response")
def step_impl(step, exp_status_code):
    """
    :type step: lettuce.core.Step
    """
    print world.user_post_response.data
    assert_equals(world.user_post_response.status_code, int(exp_status_code))


@step("I should get a user field \'(.*)\' containing \'(.*)\'")
def step_impl(step, status, txt):
    """
    :type step: lettuce.core.Step
    """
    world.user_post_response_json = json.loads(world.user_post_response.data)
    assert_equals(world.user_post_response_json[status], txt)
