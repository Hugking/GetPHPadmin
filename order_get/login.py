
import pickle
from order.order_get.config import *
from order.chaojiying.chaojiying import *
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from PIL import Image


class login(object):
    def __init__(self):
        self.url = URL
        self.user_name = USER_NAME
        self.user_password = USER_PASSWORD
        self.chaojiying_name = CHAOJIYING_NAME
        self.chaojiying_password = CHAOJIYING_PASSWORD
        self.chaojiying_id = CHAOJIYING_ID
        self.init_browser()
        self.wait = WebDriverWait(self.browser, 20)
        self.chaojiying = Chaojiying_Client(self.chaojiying_name, self.chaojiying_password, self.chaojiying_id)

    def __del__(self):
        self.close()

    def init_browser(self):
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
    "phantomjs.page.settings.userAgent"] = \
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':
            self.browser = webdriver.Chrome()

    def open(self):
        self.browser.get(self.url)

    def loginin(self):
        self.open()
        user_name = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    '//*[@id="login_bg"]/div[1]/form/input[2]')))
        user_password = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        '//*[@id="login_bg"]/div[1]/form/input[3]')))
        yzm = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_bg"]/div[1]/form/input[4]')))
        user_name.send_keys(self.user_name)
        user_password.send_keys(self.user_password)
        yzm.click()
        self.yzm()

    def yzm(self):
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="code_img"]')))
        locations = img.location
        sizes = img.size
        rangle = (int(locations['x']), int(locations['y']), int(locations['x'] + sizes['width']),
                    int(locations['y'] + sizes['height'] ))
        screen = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screen))
        captcha = screenshot.crop(rangle)
        captcha.save("order_get/config/yzm.png")
        im = open('order_get/config/yzm.png', 'rb').read()
        yzm_data = self.chaojiying.PostPic(im, 1902)
        print('验证码:', yzm_data['pic_str'])
        self.imd_id = yzm_data['pic_id']
        yzm = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_bg"]/div[1]/form/input[4]')))
        yzm.send_keys(yzm_data['pic_str'])
        submit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_bg"]/div[1]/form/input[1]')))
        submit.click()

    def get_cookies(self):
        return self.browser.get_cookies()

    def close(self):
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')

    def login_successfully(self):
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                                    '/html/body/div[3]/div[3]/div/a'))))
        except TimeoutException:
            return False

    def main(self):
        self.loginin()
        if self.login_successfully():
            print('登录成功')

    def run(self):
        try:
            self.main()
        except UnexpectedAlertPresentException:
            print(self.browser.switch_to.alert.text)
            self.browser.switch_to.alert.accept()
            print('正在重新识别验证码')
            self.chaojiying.ReportError(self.imd_id)
            self.main()
        cookies = self.get_cookies()
        with open('order_get/config/cookies.txt', 'wb') as f:
            pickle.dump(cookies, f)


if __name__ == '__main__':
    login = login()
    login.run()
