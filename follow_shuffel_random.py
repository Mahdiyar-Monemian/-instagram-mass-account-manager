import os, random, json
from selenium import webdriver
from time import sleep, time
from modem import modem
from xpaths import xpaths

modem_password = "09128906989"

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--disable-gpu')
chrome_opt.add_argument("--window-size=360,640")
DIRNAME = os.path.dirname(os.path.abspath(__file__))
SETTING_TXT = os.path.join(DIRNAME, "follow_shuffel_random_setting.txt")
SUCCESS_TXT = os.path.join(DIRNAME, "successfulls.txt")
USERNAMES_TXT = os.path.join(DIRNAME, "users_to_follow.txt")
COOKIES_FOLDER = os.path.join(DIRNAME, "user_cookies_pc")
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


def set_driver():
    global driver
    try:
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_opt)
    except:
        driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_opt)

_users = users
x = 0
for user in users[:user_amount]:
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

