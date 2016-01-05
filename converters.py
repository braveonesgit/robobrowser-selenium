from copy import deepcopy
from requests.cookies import create_cookie

from example_cookies import selenium_cookies_sample


class CookieConverter:
    @classmethod
    def to_selenium(cls, request_cookies, selenium_existing=None):
        if not selenium_existing:
            selenium_existing = selenium_cookies_sample
        for r_key in list(dict(request_cookies)):
            updated = False
            for cookie in selenium_existing:
                if cookie.get('name') == r_key:
                    cookie.update({'name': r_key})
                    cookie.update({'value': request_cookies[r_key]})
                    updated = True
            if not updated:
                tmp = deepcopy(selenium_existing[0])
                tmp.update({'name': r_key})
                tmp.update({'value': request_cookies[r_key]})
                assert tmp != selenium_existing[0]
                selenium_existing.append(tmp)
        return selenium_existing

    @classmethod
    def to_requests(cls, selenium_cookies):
        # cookie_list = []
        # for cookie in selenium_cookies:
        #     name = cookie.pop('name')
        #     value = cookie.pop('value')
        #     expires = cookie.pop('expiry')
        #     http_only = cookie.pop('httpOnly')
        #     if http_only:
        #         rest = {'HttpOnly':http_only}
        #         cookie.update(rest=rest)
        #     try:
        #         cookie_list.append(create_cookie(name=name, value=value,
        #                                          expires=expires, **cookie))
        #     except TypeError as e:
        #         raise TypeError('Cookie: {}\nOriginal error: {}'.format(cookie, e))
        # return cookie_list
        return [{cookie['name'], cookie['value']} for cookie in selenium_cookies]