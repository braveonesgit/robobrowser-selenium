from selenium.webdriver import Firefox, Chrome

from config import memberships_url
from sessions import RobobrowserSession, SeleniumSession


def is_selenium(session):
    return session in [Firefox, Chrome]


class Controller:
    def __init__(self, session=None, **kwargs):
        if is_selenium(session):
            self.session = SeleniumSession(session, *kwargs)
        else:
            self.session = RobobrowserSession(**kwargs)

    def switch(self, session, **kwargs):
        if is_selenium(session):
            self.session.close()
            self.session = SeleniumSession(session, **kwargs)
        else:
            self.session = session(**kwargs)

    @staticmethod
    def spawn(session=None, **kwargs):
        if is_selenium(session):
            return SeleniumSession(session, **kwargs)
        return RobobrowserSession(**kwargs)


def test_spawn_robo_to_sele():
    controller = Controller(login=True)
    robo_session = controller.session

    ff_session = controller.spawn(Firefox, cookies=robo_session.get_cookies())
    ff_session.visit(memberships_url)
    import pdb; pdb.set_trace()
    assert 'title' == ff_session.page_title


def test_spawn_sele_to_robo():
    controller = Controller(Firefox, login=True)
    robo_session = controller.spawn(cookies=controller.session.get_cookies())
    import pdb; pdb.set_trace()
    robo_session.visit(memberships_url)
    assert robo_session.status_code == 200
    assert 'admin/memberships' in robo_session.driver.url


def test_spawn_chrome_to_firefox():
    controller = Controller(Chrome, login=True)
    crm_session = controller.session
    print(crm_session.get_cookies())
    ff_session = controller.spawn(Firefox, cookies=crm_session.get_cookies())
    ff_session.visit(memberships_url)
    print(ff_session.get_cookies())
    assert 'foo' == ff_session.page_title


def test_spawn_ff_to_chrome():
    controller = Controller(Firefox, login=True)
    ff_session = controller.session

    chrome_session = controller.spawn(Chrome, cookies=ff_session.get_cookies())
    chrome_session.visit(memberships_url)
    assert 'foo' == chrome_session.page_title


def test_switch_ff_to_chrome():
    controller = Controller(Firefox, login=True)
    ff_session = controller.session

    controller.switch(Firefox, cookies=ff_session.get_cookies())
    controller.session.visit(memberships_url)
    assert 'foo' == controller.session.page_title


# cache?
print('start')
test_spawn_robo_to_sele()
print('done robobrowser ~> ff')
# test_spawn_sele_to_robo()
# print('done ff ~> robobrowser')
# test_spawn_chrome_to_firefox()
# print('done chrome ~> firefox')
# test_spawn_ff_to_chrome()
# print('done ff ~> chrome')
# test_switch_ff_to_chrome()
# print('done robo -> ff')
