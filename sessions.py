from robobrowser import RoboBrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from http.cookiejar import CookieJar
from requests.cookies import merge_cookies
from requests.packages.urllib3 import disable_warnings

from converters import CookieConverter
from config import credentials, help_url, login_url

disable_warnings()


class RobobrowserSession:
    def __init__(self, login=False, cookies=None):
        self.driver = RoboBrowser(
            parser='html.parser', history=True,
            allow_redirects=True, tries=5, multiplier=1
        )
        if login:
            self.login()
        if cookies:
            self.set_cookies(cookies)

    def login(self):
        self.driver.open(login_url)
        form = self.driver.get_form()
        form['username'].value = credentials['username']
        form['password'].value = credentials['password']
        self.driver.submit_form(form)
        assert self.status_code == 200

    def visit(self, url):
        self.driver.open(url, verify=False)

    def get_cookies(self):
        return self.driver.session.cookies

    def set_cookies(self, cookies):
        # if not isinstance(cookies, CookieJar):
        cookies = CookieConverter.to_requests(cookies)
        self.driver.session.cookies.update(cookies)
        # for cookie in cookies:
        # self.driver.session.cookies.update(merge_cookies(self.get_cookies(),
        #                                                  cookies))

    @property
    def status_code(self):
        return self.driver.response.status_code


class SeleniumSession:
    def __init__(self, browser, login=False, cookies=None, **kwargs):
        self.driver = browser(**kwargs)
        if login:
            self.login()
        if cookies:
            self.set_cookies(cookies)

    def login(self):
        self.driver.get(login_url)
        self.driver.find_element(By.CSS_SELECTOR, 'a.accordion-toggle').click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'username')))
        self.driver.find_element(By.NAME, 'username').send_keys(credentials['username'])
        self.driver.find_element(By.NAME, 'password').send_keys(credentials['password'])
        self.driver.find_element(By.ID, 'continue').click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, 'continue')))

    def visit(self, url):
        self.driver.get(url)

    def get_cookies(self):
        return self.driver.get_cookies()

    def set_cookies(self, cookies):
        if 'domain' not in self.driver.current_url:
            self.visit(help_url)
        if not isinstance(cookies, list):
            cookies = CookieConverter.to_selenium(cookies, self.get_cookies())
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    @property
    def page_title(self):
        return self.driver.find_element_by_css_selector(
            'html head title').get_attribute("innerHTML")

    def close(self):
        self.driver.close()
        print('Closed: {}'.format(self.driver.capabilities['browserName']))

    def __del__(self):
        try:
            self.driver.close()
            print('Closed: {}'.format(self.driver.capabilities['browserName']))
        except ConnectionRefusedError:
            pass


class RequestsSession:
    def __init__(self):
        pass
