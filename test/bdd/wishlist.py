import json

from lettuce import step, world, before
from nose.tools import assert_equals

from app import create_app


@before.all
def before_all():
    app = create_app()
    world.app = app.test_client()


""" Create Wishlist """



@step('I have the details of wishlist')
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    world.wishlist1 = step.hashes[0]


@step("I POST to url \'(.*)\' the wishlist")
def step_impl(step, url):
    """
    :type step: lettuce.core.Step
    """
    world.wishlist_post_uri = url
    world.wishlist_post_response = world.browser.post(world.wishlist_post_uri, data=json.dumps(world.wishlist1))


@step("I should get status code response \'(.*)\'")
def step_impl(step, expected_status_code):
    """
    :param expected_status_code:
    :type step: lettuce.core.Step
    """
    assert_equals(world.wishlist_post_response.status_code, int(expected_status_code))


@step("I should get \'(.*)\' status")
def step_impl(step, status):
    """
    :type step: lettuce.core.Step
    """
    # raise Exception(json.loads(world.wishlist_post_response.data))
    world.wishlist_post_response_json = json.loads(world.wishlist_post_response.data)
    assert_equals(world.wishlist_post_response_json['status'], status)


@step("I should get \'(.*)\' message")
def step_impl(step, message):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.wishlist_post_response_json['message'], message)

    


""" Get Wishlist - sunny case """


@step("wishlist \'(.*)\' is in the system")
def given_wishlist_is_in_the_system(step, wishlist_id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.resp = world.browser.get('/api/v1/wishlist/'.format(wishlist_id))
    # raise Exception(json.loads(world.resp.data))
    data = json.loads(world.resp.data)
    assert_equals(data['status'], 'ok')


@step("I retrieve the wishlist \'(.*)\'")
def when_I_retrieve_the_wishlist(step, wishlist_id):
    """
    :param id:
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get('/api/v1/wishlist/'.format(wishlist_id))


@step("I should have a status code response \'(.*)\'")
def then_i_should_have_a_status_code_response_200(step, expected_status_code):
    """
    :param expected_status_code:
    :type step: lettuce.core.Step
    """
    assert_equals(world.response.status_code, int(expected_status_code))



@step("the following details are returned :")
def and_the_following_details_are_returned(step):
    """
    :type step: lettuce.core.Step
    """
    resp = world.response.data
    assert_equals(world.resp.data, resp)


""" Get Wishlist - rainy case """


@step("I retrieve a wishlist with id \'(.*)\'")
def given_I_retrieve_a_wishlist_with_id(step, wishlist_id):
    """
    :param url:
    :type step: lettuce.core.Step
    """
    world.wishlist_uri = '/api/v1/wishlists/%s/' % (wishlist_id)


@step("I retrieve the wishlist JSON result")
def when_I_retrieve_the_wishlist_JSON_result(step):
    """
    :type step: lettuce.core.Step
    """
    world.response = world.browser.get(world.wishlist_uri)


@step("I should have a status code response \'(.*)\'")
def step_impl(step, expected_status_code):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.response.status_code, int(expected_status_code))


@step("I should get the status says 'ok'")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp['status'], 'ok')


@step("it should  have a field count '0'")
def and_it_should_have_a_field_count_0(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(world.resp['count'], '0')


@step("it should  have a field message saying 'No entries found'")
def and_it_should_have_a_field_message_saying_no_entries_found(step):
    """
    :type step: lettuce.core.Step
    """
    world.resp = json.loads(world.response.data)
    assert_equals(world.resp['message'], 'No entries found')


@step("it should  have an empty field 'entries'")
def and_it_should_have_an_empty_field_entries(step):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(len(world.resp['entries']), 0)



# Create an invalid wishlist - rainy case
#     Given I have the details of wishlist
#     |wishlist_id | wishlist_name |
#     | noob | 1 |
#     When I POST to url '/api/v1/wishlist/' the wishlist
#     Then I should get '200' status code response
#     And I should get 'ok' status
#     And I should get 'error' message

