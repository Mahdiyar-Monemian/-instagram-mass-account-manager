import os, random, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, time
from modem import modem
from xpaths import xpaths

modem_password = "09128906989"

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
SETTING_TXT = os.path.join(DIRNAME, "follow_shuffel_random_setting.txt")
SUCCESS_TXT = os.path.join(DIRNAME, "successfulls.txt")
USERNAMES_TXT = os.path.join(DIRNAME, "users_to_follow.txt")
COOKIES_FOLDER = os.path.join(DIRNAME, "user_cookies_android")
MOBILE_FOLDER = os.path.join(DIRNAME, "user_phones");
chromedriver = os.path.join(DIRNAME, "chromedriver.exe")

users_to_follow = []
with open(USERNAMES_TXT, 'r') as fp:
    for line in fp.read().splitlines():
        users_to_follow.append(line)

users = []
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

with open(SETTING_TXT, 'r') as fb:
    lines = fb.read().splitlines()
    nmodem = int(lines[1])
    after_account_wait_min = float(lines[3])
    after_account_wait_max = float(lines[5])
    after_follow_wait_min = float(lines[7])
    after_follow_wait_max = float(lines[9])
    user_amount = lines[11]
    if(user_amount == "all"):
        user_amount = len(users)
    else:
        user_amount = int(user_amount)
    user_to_follow_amount = int(lines[13])

print(f"""
modem reset: {nmodem}
time sleeping after account: {after_account_wait_min} - {after_account_wait_max}
time sleeping after follow: {after_follow_wait_min} - {after_follow_wait_max}
amount of account: {user_amount}
amount of account to follow: {user_to_follow_amount}
""")

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

def update_successfulls(_list):
    with open(SUCCESS_TXT, 'w') as fb:
        text = ""
        for user in _list:
            text += f"{user[0]}, {user[1]}, {user[2]}\n"
        fb.write(text)

random.shuffle(users)
for usr in users:
    print(usr[0])

update_successfulls(users)


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


def set_driver(user):
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

_users = users
x = 0
for user in users[:user_amount]:
    x += 1
    set_driver(user[0])
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
            random.shuffle(users_to_follow)
            for username in users_to_follow[:user_to_follow_amount]:
                print(f"trying to follow {username}")
                driver.get(f"https://www.instagram.com/{username}/")
                sleep(5)
                click_by_xpath(xpaths["follow_1"], waituntil=False)
                click_by_xpath(xpaths["follow_2"], waituntil=False)

                t = random.uniform(after_follow_wait_min, after_follow_wait_max)
                print(f"Sleeping for {t} seconds\n")
                sleep(t)
            
            _users.remove(user)
            update_successfulls(_users)
            print(f"{user[0]} has been removed")
            save_cookies(user[0])
            t = random.uniform(after_account_wait_min, after_account_wait_max)
            print(f"Sleeping for {t} seconds")
            sleep(t)
            break

        except TimeoutError: print("TIME OUT")
        except: print("SOME ERROR")
        save_cookies(user[0])

    save_cookies(user[0])
    try:
        driver.quit()
        driver = None
        del driver
    except: pass
    try:
        if(x % nmodem == 0):
            modem()
    except: print("couldn't restart modem")

    # driver.get(f"https://www.instagram.com/{user[0]}/")
    # photo = r"C:\Users\Mahdiyar\Desktop\photo_2020-04-14_14-57-29.jpg"
    # send_by_xpath(xpaths["profile_picture"], photo, 20)
    # print("end")

