from copy import deepcopy
# from requests.cookies import create_cookie

from example_cookies import selenium_cookies_sample


class CookieConverter:
    @classmethod
    def to_selenium(cls, cookiejar, selenium_cookies=None):
        if not selenium_cookies:
            selenium_cookies = selenium_cookies_sample
        for r_key in list(dict(cookiejar)):
            updated = False
            for cookie in selenium_cookies:
                if cookie.get('name') == r_key:
                    cookie.update({'name': r_key})
                    cookie.update({'value': cookiejar[r_key]})
                    updated = True
            if not updated:
                tmp = deepcopy(selenium_cookies[0])
                tmp.update({'name': r_key})
                tmp.update({'value': cookiejar[r_key]})
                assert tmp != selenium_cookies[0]
                selenium_cookies.append(tmp)
        return selenium_cookies

    @classmethod
    def to_requests(cls, selenium_cookies):
        return [{c['name']: c['value']} for c in selenium_cookies]
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
