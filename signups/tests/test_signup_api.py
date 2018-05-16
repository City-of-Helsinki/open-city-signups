import pytest
from django.utils.timezone import now
from rest_framework.reverse import reverse

from signups.models import Signup
from signups.tests.factories import SignupFactory
from signups.tests.utils import check_disallowed_methods, delete, get, post

LIST_URL = reverse('signup-list')


def get_detail_url(obj):
    return reverse('signup-detail', kwargs={'pk': obj.id})


def check_signup_data(data, obj):
    assert set(data.keys()) == {'id', 'target', 'created_at', 'cancelled_at'}

    assert data['id'] == obj.id
    assert data['target'] == obj.target.identifier


def test_unauthenticated_user_cannot_access(api_client):
    get(api_client, LIST_URL, 401)


def test_disallowed_methods(user_api_client, signup):
    list_disallowed_methods = ('put', 'patch', 'delete')
    check_disallowed_methods(user_api_client, LIST_URL, list_disallowed_methods)

    detail_disallowed_methods = ('post', 'put', 'patch')
    check_disallowed_methods(user_api_client, get_detail_url(signup), detail_disallowed_methods)


def test_get_signup_list(user_api_client, signup):
    data = get(user_api_client, LIST_URL)
    signup_data = data['results'][0]
    check_signup_data(signup_data, signup)


def test_get_signup_detail(user_api_client, signup):
    signup_data = get(user_api_client, get_detail_url(signup))
    check_signup_data(signup_data, signup)


def test_user_can_see_only_own_signups(user_api_client, signup):
    other_user_signup = SignupFactory()

    data = get(user_api_client, LIST_URL)
    results = data['results']
    assert len(results) == 1
    assert results[0]['id'] == signup.id

    get(user_api_client, get_detail_url(other_user_signup), status_code=404)


def test_post_signup(user_api_client, signup_target):
    assert Signup.objects.count() == 0

    post(user_api_client, LIST_URL, {'target': signup_target.identifier})

    assert Signup.objects.count() == 1
    new_signup = Signup.objects.latest('id')
    assert new_signup.user == user_api_client.user
    assert new_signup.target == signup_target
    assert new_signup.cancelled_at is None
    assert new_signup.created_at


def test_post_signup_nonexisting_target(user_api_client):
    assert Signup.objects.count() == 0

    data = post(user_api_client, LIST_URL, {'target': 'foobar'}, status_code=400)
    assert 'target' in data


def test_post_already_existing_signup(user_api_client, signup, signup_target):
    assert Signup.objects.count() == 1

    post(user_api_client, LIST_URL, {'target': signup_target.identifier}, status_code=409)

    assert Signup.objects.count() == 1


def test_delete_signup(user_api_client, signup):
    assert Signup.objects.count() == 1
    assert Signup.objects.filter(cancelled_at=None).count() == 1

    delete(user_api_client, get_detail_url(signup))

    assert Signup.objects.count() == 1
    assert Signup.objects.filter(cancelled_at=None).count() == 0

    signup.refresh_from_db()
    assert signup.cancelled_at


def test_cannot_delete_other_user_signup(user_api_client):
    other_user_signup = SignupFactory()

    delete(user_api_client, get_detail_url(other_user_signup), status_code=404)

    Signup.objects.get(id=other_user_signup.id)


def test_cannot_delete_already_cancelled_signup(user_api_client):
    signup = SignupFactory(user=user_api_client.user, cancelled_at=now())

    delete(user_api_client, get_detail_url(signup), status_code=404)


def test_cancelled_signups_not_visible_by_default(user_api_client):
    cancelled_signup = SignupFactory(user=user_api_client.user, cancelled_at=now())

    list_data = get(user_api_client, LIST_URL)
    assert len(list_data['results']) == 0

    get(user_api_client, get_detail_url(cancelled_signup), 404)


@pytest.mark.parametrize('true_value', (
    '=True',
    '=true',
    '=1',
    '=',
    '',
    '=actually_anything_goes',
))
def test_include_cancelled_filter(user_api_client, signup, true_value):
    cancelled_signup = SignupFactory(user=user_api_client.user, cancelled_at=now())

    list_data = get(user_api_client, LIST_URL + '?include_cancelled{}&foo=bar'.format(true_value))
    assert len(list_data['results']) == 2

    list_data = get(user_api_client, LIST_URL + '?include_cancelled=false')
    assert len(list_data['results']) == 1
    assert list_data['results'][0]['id'] != cancelled_signup.id

    detail_data = get(user_api_client, get_detail_url(cancelled_signup) + '?include_cancelled{}'.format(true_value))
    assert detail_data['id'] == cancelled_signup.id


def test_target_filter(user_api_client, signup):
    other_target_signup = SignupFactory(user=user_api_client.user)

    list_data = get(user_api_client, LIST_URL)
    assert len(list_data['results']) == 2

    list_data = get(user_api_client, LIST_URL + '?target={}'.format(other_target_signup.target.identifier))
    assert len(list_data['results']) == 1
    assert list_data['results'][0]['id'] == other_target_signup.id
