import os, random, glob, json
from selenium import webdriver
from time import sleep, time
from xpaths import xpaths
from modem import modem
import pyautogui

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--disable-gpu')
chrome_opt.add_argument("--window-size=360,640")
DIRNAME = os.path.dirname(os.path.abspath(__file__))
COOKIES_FOLDER = os.path.join(DIRNAME, "user_cookies_pc")

SUCCESS_TXT = os.path.join(DIRNAME, "successfulls.txt")
SETTING_TXT = os.path.join(DIRNAME, "prof_and_bio_setting.txt")
BIOS_TXT = os.path.join(DIRNAME, 'bios.txt')
chromedriver = os.path.join(DIRNAME, "chromedriver.exe")

photos_D = glob.glob(f"{DIRNAME}\Photos_D\*")
photos_P = glob.glob(f"{DIRNAME}\Photos_P\*")

with open(BIOS_TXT, 'r', encoding='utf-8') as fb:
    bios = fb.read().splitlines()

with open(SETTING_TXT, 'r') as fb:
    lines = fb.read().splitlines()
    nmodem = int(lines[1])
    prof_wait_min = float(lines[3])
    prof_wait_max = float(lines[5])

print(f"""
modem reset: {nmodem}
prof wait: {prof_wait_min} - {prof_wait_max}
""")

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

def json_cookie_path_of(user):
    return os.path.join(COOKIES_FOLDER, f"{user}.json")


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
            text_area = driver.find_element_by_xpath(xpath)
            text_area.clear()
            text_area.send_keys(text)
            sleep(wait) 
            break
        except:
            sleep(0.5)
            if(not waituntil):
                break

driver = None
def set_driver():
    global driver
    try:
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_opt)
    except:
        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_opt)

def close_driver():
    global driver
    try:
        driver.quit()
        driver = None
        del driver
    except: pass

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

x = 0
for user in users:
    x += 1
    set_driver()
    print(user[0])
    for y in range(3):
        load_cookies(user[0])
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
            driver.get(f"https://www.instagram.com/{user[0]}/")
            if(user[2] == 'D'):
                photo = random.choice(photos_D)
            else:
                photo = random.choice(photos_P)
            print(photo)
            click_by_xpath(xpaths["profile_picture"], 3)
            pyautogui.write(photo)
            pyautogui.press('enter')
            sleep(4)
            
            bio = random.choice(bios)
            driver.get("https://www.instagram.com/accounts/edit/")
            driver.find_element_by_xpath(xpaths["bio"]).clear()
            send_by_xpath(xpaths["bio"], bio)
            click_by_xpath(xpaths["bio_submit"], 3)
            print("done")
            sleep(random.uniform(prof_wait_min, prof_wait_min))
            save_cookies(user[0])
            break

        except TimeoutError: print("Timeout")
        except: print("some error")

    save_cookies(user[0])
    try:
        close_driver()
        if(x % nmodem == 0):
            print("I have to reset the modem")
            modem()
    except:print("couldn't restart modem")




