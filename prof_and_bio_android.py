import os, random, glob, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, time
from xpaths import xpaths
from modem import modem
import pyautogui

userAgents = [
    "Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; Micromax A76 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-A320FL Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/9.4 Chrome/67.0.3396.87 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-A320F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 4.4.4; SAMSUNG SM-J100F Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.0 Chrome/34.0.1847.76 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 510)",
    "Mozilla/5.0 (Linux; Android 8.0.0; Pixel Build/OPR6.170623.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Pixel Build/OPM1.171019.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Pixel Build/NOF26V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; Pixel Build/OPR3.170623.013) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Pixel Build/OPM2.171019.029) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.126 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 4.4.2; SM-N9006 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36",
    "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 820; Vodafone) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
    "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 820) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537",
    "Mozilla/5.0 (Linux; U; Android 2.3.5; fr-fr; GT-I9000-ORANGE/I9000BVJVC Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.3; pt-br; GT-I9000B Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; pt-pt; GT-I9000 Build/JDQ39E) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 CyanogenMod/10.1.2/galaxysmtd",
]

DIRNAME = os.path.dirname(os.path.abspath(__file__))
COOKIES_FOLDER = os.path.join(DIRNAME, "user_cookies_android")
MOBILE_FOLDER = os.path.join(DIRNAME, "user_phones");
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

def txt_mobile_path_of(user):
    return os.path.join(MOBILE_FOLDER, f"{user}.txt")

def save_mobile(user, user_agent):
    MOBILE_PATH = txt_mobile_path_of(user)
    with open(MOBILE_PATH, 'w') as fp:
        fp.write(user_agent)

def load_mobile(user):
    MOBILE_PATH = txt_mobile_path_of(user)
    try:
        with open(MOBILE_PATH) as fp:
            return fp.read()
    except:
        return None

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
    user_agent = load_mobile(user)
    if user_agent == None:
        print(f"No existing user agent for {user}")
        user_agent = random.choice(userAgents)
        save_mobile(user, user_agent)

    mobile_emulation = {
        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        "userAgent": user_agent,
    }
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=360,640")
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)  
    try:
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    except:
        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)

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
        try:
            driver.get("https://www.google.com/")            
            cookies_been_load = load_cookies(user[0])
            print(user[0])
            driver.get("https://www.instagram.com/")
            if not cookies_been_load:
                click_by_xpath(xpaths["android_login"], 3)
                send_by_xpath(xpaths["android_username_1"], user[0], 0.5, waituntil=False)
                send_by_xpath(xpaths["android_password_1"], user[1], 0.7, waituntil=False)
                send_by_xpath(xpaths["android_username_2"], user[0], 0.5, waituntil=False)
                send_by_xpath(xpaths["android_password_2"], user[1], 0.7, waituntil=False)
                click_by_xpath(xpaths["android_submit_1"], 3, waituntil=False)
                click_by_xpath(xpaths["android_submit_2"], 3, waituntil=False)
                click_by_xpath(xpaths["android_info_notnow"], 2)
            driver.get(f"https://www.instagram.com/{user[0]}/")
            if(user[2] == 'D'):
                photo = random.choice(photos_D)
            else:
                photo = random.choice(photos_P)
            print(photo)
            click_by_xpath(xpaths["profile_picture"], 3)
            pyautogui.write(photo)
            pyautogui.press('enter')
            click_by_xpath(xpaths['android_save_photo'])
            sleep(4)
            
            bio = random.choice(bios)
            driver.get("https://www.instagram.com/accounts/edit/")
            driver.find_element_by_xpath(xpaths["bio"]).clear()
            send_by_xpath(xpaths["bio"], bio)
            click_by_xpath(xpaths["bio_submit"], 3)
            save_cookies(user[0])
            print("done")
            sleep(random.uniform(prof_wait_min, prof_wait_min))
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




