import browser
import time

class HSW:
    def __init__(self, captcha_url):
        self.browser = browser.create_browser(False)
        self.loaded = False
        self.setup_browser(captcha_url)

    def setup_browser(self, captcha_url):
        self.browser.get(captcha_url)
        time.sleep(3)
        if browser.trigger_captcha(self.browser):
            time.sleep(5)
            if browser.hook_to_challenge(self.browser):
                print("[LOG]: Succesfully hooked onto HSW frame! \n")
                self.loaded = True
                return
        print("[WARNING] Defaulting to regular HSW generation")
        # not implemented yet

    def generate_hsw(self, jwt):
        n = self.browser.execute_script('return hsw("{}")'.format(jwt))
        print(n)
        return n