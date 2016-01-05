
requests_cookies_sample = {
    'sessionid': 'foo',
    'csrftoken': 'bar'
}

selenium_cookies_sample = [
    {
        'name': 'foo',
        'secure': False,
        'httpOnly': False,
        'domain': 'bar.com',
        'value': 'bar',
        'expiry': 1111111111,
        'path': '/'
    },
    {
        'name': 'sessionid', 'secure': False, 'httpOnly': True,
        'domain': 'foo.com',
        'value': 'bar', 'expiry': 1111111111,
        'path': '/'
    }
]
