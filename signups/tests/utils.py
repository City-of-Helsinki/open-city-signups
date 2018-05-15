def get(api_client, url, status_code=200):
    response = api_client.get(url)
    assert response.status_code == status_code, 'Expected status code {} but got {} with data {}'.format(
        status_code, response.status_code, response.data)
    return response.data


def post(api_client, url, data=None, status_code=201):
    response = api_client.post(url, data)
    assert response.status_code == status_code, 'Expected status code {} but got {} with data {}'.format(
        status_code, response.status_code, response.data)
    return response.data


def delete(api_client, url, status_code=204):
    response = api_client.delete(url)
    assert response.status_code == status_code, 'Expected status code {} but got {} with data {}'.format(
        status_code, response.status_code, response.data)
    return response.data


def check_disallowed_methods(api_client, urls, methods, status_code=405):
    if isinstance(urls, str):
        urls = (urls,)
    if isinstance(methods, str):
        methods = (methods,)

    for url in urls:
        for method in methods:
            response = getattr(api_client, method)(url)
            assert response.status_code == status_code, (
                '%s %s expected %s, but got %s %s' % (method, url, status_code, response.status_code, response.data)
            )
