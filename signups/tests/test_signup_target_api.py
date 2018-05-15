from rest_framework.reverse import reverse

from signups.tests.utils import check_disallowed_methods, get

LIST_URL = reverse('signuptarget-list')


def get_detail_url(obj):
    return reverse('signuptarget-detail', kwargs={'identifier': obj.identifier})


def check_signup_target_data(data, obj):
    assert set(data.keys()) == {'id', 'name'}

    assert data['id'] == obj.identifier
    assert data['name'] == obj.name


def test_disallowed_methods(user_api_client, signup_target):
    disallowed_methods = ('post', 'put', 'patch', 'delete')
    urls = (LIST_URL, get_detail_url(signup_target))

    check_disallowed_methods(user_api_client, urls, disallowed_methods)


def test_get_signup_target_list(api_client, signup_target):
    data = get(api_client, LIST_URL)
    signup_target_data = data['results'][0]
    check_signup_target_data(signup_target_data, signup_target)


def test_get_signup_target_detail(api_client, signup_target):
    signup_target_data = get(api_client, get_detail_url(signup_target))
    check_signup_target_data(signup_target_data, signup_target)
