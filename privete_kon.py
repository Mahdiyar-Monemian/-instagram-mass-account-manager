import os, random, json
from selenium import webdriver
from time import sleep, time
from xpaths import xpaths
from modem import modem
from selenium.webdriver.chrome.options import Options
import pyautogui

DIRNAME = os.path.dirname(os.path.abspath(__file__))
SUCCESS_TXT = os.path.join(DIRNAME, "successfulls.txt")
SETTING_TXT = os.path.join(DIRNAME, "privete_kon_setting.txt")
COOKIES_FOLDER = os.path.join(DIRNAME, "user_cookies_pc")
chromedriver = os.path.join(DIRNAME, "chromedriver.exe")

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size=360,640") 

with open(SETTING_TXT, 'r') as fb:
    lines = fb.read().splitlines()
    nmodem = int(lines[1])
    wait_min = float(lines[3])
    wait_max = float(lines[5])

users = []
_user = None
with open(SUCCESS_TXT, 'r') as fb:
    jump_next_line = False;
    for line in fb.read().splitlines():
        if jump_next_line:
            users.append((_user[0], _user[1], line.split(' ')[1]))
            jump_next_line = False
            continue
        elif line[-1] == 'D' or line[-1] == 'P':
            line = line.split(' ')
            users.append((line[0][:-1], line[1][:-1], line[2]))
        else:
            line = line.split(' ')
            _user = (line[0][:-1], line[1])
            jump_next_line = True;



def click_by_xpath(xpath, wait = 0, waituntil = True):
    start_time = time()    
    while(True):
        if(time() - start_time > 40):
            raise TimeoutError
            break
        try:
            driver.find_element_by_xpath(xpath).click()
            sleep(wait)
            break
        except:
            sleep(0.5)
            if(not waituntil):
                break


def send_by_xpath(xpath, text, wait = 0, waituntil = True):
    start_time = time()    
    while(True):
        if(time() - start_time > 40):
            raise TimeoutError
            break
        try:
            driver.find_element_by_xpath(xpath).send_keys(text)
            sleep(wait) 
            break
        except:
            sleep(0.5)
            if(not waituntil):
                break

def json_cookie_path_of(user):
    return os.path.join(COOKIES_FOLDER, f"{user}.json")

def load_cookies(user):
    global driver
    COOKIE_PATH = json_cookie_path_of(user)
    try:
        with open(COOKIE_PATH) as fp:
            driver.delete_all_cookies()
            for cookie in json.load(fp):
                driver.add_cookie(cookie)
            return True
    except:
        print(f"No existing cookie for {user}")
        return False

def save_cookies(user):
    global driver
    COOKIE_PATH = json_cookie_path_of(user)
    with open(COOKIE_PATH, 'w') as fp:
        json.dump(driver.get_cookies(), fp)

def set_driver():
    global driver 
    try:
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    except:
        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

driver = None

x = 0
for user in users:
    print(user[0])
    x += 1
    set_driver()
    for y in range(3):
        try:
            driver.get("https://www.google.com/")
            cookies_been_load = load_cookies(user[0])
            print(user[0])
            driver.get("https://www.instagram.com/")
            if not cookies_been_load:
                send_by_xpath(xpaths["login_username"], user[0], 0.5)
                send_by_xpath(xpaths["login_password"], user[1], 0.7)
                click_by_xpath(xpaths["login_submit"])
                click_by_xpath(xpaths["login_info_notnow"], 1)
                click_by_xpath(xpaths["notification_notnow"], 1)
            driver.get("https://www.instagram.com/accounts/privacy_and_security/")
            click_by_xpath(xpaths["privet_tik"], 3)
            print(f"successfully priveted the account for {user[0]}\n")

            t = random.uniform(wait_min, wait_max)
            print(f"Sleeping for {t} seconds")
            sleep(t)
            break

        except: print("some error")

    try:
        driver.quit()
        driver = None
        del driver
    except: pass
    try:
        if(x % nmodem == 0):
            modem()
    except: print("couldn't restart modem")


