import os, time
from time import sleep
from selenium import webdriver

DIRNAME = os.path.dirname(os.path.abspath(__file__))
chromedriver = os.path.join(DIRNAME, "chromedriver.exe")
modem_password = "09128906989"
chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--disable-gpu')
# driver = None

def set_driver():
    global driver
    try:
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_opt)
    except:
        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_opt)

def try_quit_driver():
    global driver
    try:
        driver.quit()
        driver = None
        del driver
    except: pass

def modem():
    print("Restarting modem")
    try_quit_driver()
    set_driver()
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.get("http://192.168.0.1/index.html#login")
    sleep(10)
    driver.find_element_by_id("txtPwd").send_keys(modem_password)
    driver.find_element_by_id("btnLogin").click()
    sleep(2)
    driver.get("http://192.168.0.1/index.html#restart")
    sleep(1)
    driver.find_element_by_xpath('//input[@value="Restart"]').click()
    driver.find_element_by_id("yesbtn").click()
    sleep(15)
    while True:
        try:
            driver.find_element_by_id("okbtn").click()
            print("I turned off internet")
            break
        except:
            sleep(1)

    driver.get("http://192.168.0.1/index.html#login")
    driver.find_element_by_id("txtPwd").send_keys(modem_password)
    driver.find_element_by_id("btnLogin").click()
    sleep(40)
    start_time = time.time()
    while True:
        if(time.time() - start_time > 180):
            print("net is on")
            break
        try:
            try:
                driver.find_element_by_css_selector("i.signal.signal5")
            except:
                driver.find_element_by_css_selector("i.signal.signal4")
            print("net is on")
            break
        except:
            sleep(1)
    try_quit_driver()
