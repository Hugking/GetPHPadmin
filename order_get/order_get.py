from order.order_get.login import *
from order.order_get.config import *
class order_get(object):
    def __init__(self):
        self.url = 'http://cenxin.suuci.com/admin.php?m=index'
        self.init_browser()
        self.wait = WebDriverWait(self.browser, 20)

    def __del__(self):
        self.close()

    def init_browser(self):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = \
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':
            self.browser = webdriver.Chrome()

    def open_and_add_cookies(self):
        self.browser.get(URL)
        with open('order_get/config/cookies.txt', 'rb') as f:
            cookies = pickle.load(f)
        for item in cookies:
            self.browser.add_cookie(item)
        self.browser.get(self.url)

    def order_get_and_write_file(self):
        order_select = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="M3"]/a')))
        order_select.click()
        self.browser.switch_to.frame('rightMain')
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="end_time"]')))
        time = self.browser.find_element_by_xpath('//*[@id="end_time"]').get_attribute('value')
        print('当前日期', time)
        with open('order_get/order_data/'+time + '.txt', 'w') as f:
            while 1:
                self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                '/html/body/div[3]/div/table/tbody')))
                for i in range(1, 21):
                    data = self.browser.find_element_by_xpath('/html/body/div[3]/div/table/tbody/tr'+'[' + str(i) + ']')
                    s = data.text.split(' ')
                    while s[8] == time:
                        f.write(data.text.replace(' ', ',') + '\n')
                        print(data.text)
                        if s[8] != time:
                            break
                        break
                next = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                '/html/body/div[3]/div/div/div/a[23]')))
                next.click()
                break

    def close(self):
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')

    def run(self):
        self.open_and_add_cookies()
        self.order_get_and_write_file()


if __name__ == '__main__':
    order_get().run()