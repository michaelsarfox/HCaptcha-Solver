from selenium.webdriver.common.by import By
import undetected_chromedriver

def get_arguments():
    return [
        "--lang=en-US",
        "--disable-encryption",
        "--font-masking-mode=3",
        "--flag-switches-begin",
        "--flag-switches-end",
        "--enable-quic",
        "--enable-tcp-fast-open",
        "--disable-remote-fonts",
        "--disable-background-networking",
        "--disable-extensions",
        "--no-first-run",
        "--no-sandbox",
        "--disable-web-security",
        "--allow-running-insecure-content"
        "--disable-infobars",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled"
    ]

def create_chrome_options():
    options = undetected_chromedriver.options.ChromeOptions()
    for argument in get_arguments():
        options.add_argument(argument)
    return options

def create_browser(headless = True):
    return undetected_chromedriver.Chrome(headless = headless, options = create_chrome_options())

def trigger_captcha(browser: undetected_chromedriver.Chrome):
    checkbox = browser.find_element(By.XPATH, "//iframe[contains(@title,'checkbox')]")
    if not checkbox:
        print("[ERROR] Failed to locate the captcha box.")
        return False
    checkbox.click()
    return True

def hook_to_challenge(browser: undetected_chromedriver.Chrome):
    challenge = browser.find_element(By.XPATH, "//iframe[contains(@title,'hCaptcha challenge')]")
    if not challenge:
        print("[ERROR] Failed to hook onto HCaptcha challenge.")
        return False
    browser.switch_to.frame(challenge)
    return True
