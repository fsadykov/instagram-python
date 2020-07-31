from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import time
import json 
import os 


max_last_review = 20
max_people_list = 51
locations_check = ['bensenville', 'franklin', 'addision', 'roselle', 'northlake', 'elmhust', 'villa', 'lambard', 'schaumburg', 'rosemont']

WINDOW_SIZE = "1920,1080"

if os.environ.get('CHROMEDRIVER_PATH') and os.environ.get('ING_USERNAME') and os.environ.get('ING_PASSWORD'):
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
    USERNAME = os.environ.get('ING_USERNAME')
    PASSWORD = os.environ.get('ING_PASSWORD')
else:
    print("You are missing one of these environment variable <CHROMEDRIVER_PATH,ING_USERNAME,ING_PASSOWRD>")
    exit(1)

chrome_options = Options()  
# chrome_options.add_argument("--headless")  
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          options=chrome_options
                         )

logging.basicConfig(level=logging.WARNING)



driver.get('https://www.instagram.com')


#### Instagram login page
username = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
username.send_keys(USERNAME)

password = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
password.send_keys(PASSWORD)
password.send_keys(Keys.RETURN)

base_url = 'https://www.instagram.com'

time_to_sleep=  2 
def follow_all():
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
    except:
        return 0

    for i in range(1, 50):
        base_button_xpath = '/html/body/div[4]/div/div/div[2]/ul/div'
        try:
            try:
                driver.find_element_by_xpath(f"{base_button_xpath}/li[{i}]/div/div[2]/button")
                xpath_for_button = f"{base_button_xpath}/li[{i}]/div/div[2]/button"
            except:
                xpath_for_button = f"{base_button_xpath}/li[{i}]/div/div[3]/button"
                
            if driver.find_element_by_xpath(xpath_for_button).text.lower() == 'follow':
                
                driver.find_element_by_xpath(xpath_for_button).click()
                time.sleep(time_to_sleep)

            if driver.find_element_by_xpath(xpath_for_button).text.lower() == 'follow':
                break
        except:
            print("Can not find the element")


popular_people = [
    'jasonstatham',
    'snoopdogg',
    'djcassidy',
    'lukelintz',
    'adamquinn',
    'alldaynicco',
    'ariesspears',
    'violadavis',
    'davidalangrier',
    'starz',
    'adele',
    'arianagrande',
    'beyonce',
    'brooklynbeckham',
    'caitlynjenner',
    'calvinharris',
    'caradelevingne',
    'carolineflack',
    'cherylofficial',
    'officialdannydyer',
    'davidbeckham',
    'elliegoulding',
    'emmawatson',
    'fernemccann'
]


def run_follow():
    for username in popular_people:
        driver.get(f"{base_url}/{username}")
        follow_all()




total_user = []
for user_item in range(0, 200):
    try:
        total_user.append(driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{user_item}]/div/div[1]/div[2]/div[1]/span").text)
    except:
        pass




def save_to_file(data):
    with open('output.json', 'w') as file: 
        json.dump(data, file, indent=2)
    