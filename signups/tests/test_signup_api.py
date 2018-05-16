from rest_framework.reverse import reverse

from signups.tests.utils import check_disallowed_methods, get
from signups.tests.factories import SignupFactory

LIST_URL = reverse('signup-list')


def get_detail_url(obj):
    return reverse('signup-detail', kwargs={'pk': obj.id})


def check_signup_data(data, obj):
    assert set(data.keys()) == {'id', 'target', 'created_at', 'cancelled_at'}

    assert data['id'] == obj.id
    assert data['target'] == obj.target.identifier


def test_disallowed_methods(user_api_client, signup):
    list_disallowed_methods = ('put', 'patch', 'delete')
    check_disallowed_methods(user_api_client, LIST_URL, list_disallowed_methods)

    detail_disallowed_methods = ('post',)
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
