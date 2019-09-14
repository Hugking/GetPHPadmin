from order.order_get.login import *
from order.order_get.order_get import *
import time
if __name__ == '__main__':
    login().run()
    print('loading...(5s)')
    time.sleep(5)
    order_get().run()