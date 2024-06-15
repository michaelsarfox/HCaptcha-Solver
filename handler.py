import hsw
import sys

class Handler:
    def __init__(self):
        self.site_key = None
        self.site_host = None
        self.is_invisible = False
        self.hsw_browser = None

    def launch_hsw_browser(self, captcha_url):
        if captcha_url:
            self.hsw_browser = hsw.HSW(captcha_url)
            return self.hsw_browser.loaded
        return False

    def set_captcha_data(self, site_key, site_host, is_invisible):
        if site_key and site_key:
            self.site_key = site_key
            self.site_host = site_host
            self.is_invisible = bool(is_invisible)
            return True
        return False

    def is_browser_launched(self):
        return self.hsw_browser is not None and self.hsw_browser.loaded

    def kill_browser(self):
        if self.is_browser_launched():
            print("[LOG]: Killing HSW browser....")
            self.hsw_browser.quit()
            sys.exit(0)

    def cleanup_handler(self, signum, frame):
        print("[LOG]: Received signal {}. Cleaning up...".format(signum))
        self.kill_browser()
        sys.exit(0)