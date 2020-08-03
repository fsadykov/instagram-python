from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
import time
import json 
import os 


max_last_review = 20
max_people_list = 51
locations_check = ['bensenville', 'franklin', 'addision', 'roselle', 'northlake', 'elmhust', 'villa', 'lambard', 'schaumburg', 'rosemont']

base_users = [
    'fsadykov',
    'arianagrande',
    'khomenko_officially'
]

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

base_url = 'https://www.instagram.com'


def instagram_login():
    # Function responsible to login to instragram
    driver.get(base_url)
    try:
        ## Trying the user profile exist
        driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]')
        logging.warning("You are already login!!")
    except:

        ## Wating until login page is loaded to be able to login
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input'))
        WebDriverWait(driver, 2).until(element_present)
        
        ## Sending the username and password
        username = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
        username.send_keys(USERNAME)
        password = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
        password.send_keys(PASSWORD)
        password.send_keys(Keys.RETURN)

        try:
            ## Making sure that user is log in
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]'))
            WebDriverWait(driver, 7).until(element_present)
            logging.info("Script was able to login to system")
        except TimeoutException:
            logging.error("Script was not able to login timeout issue")
    
        


def follow_all():
    ## Following all people from 
    time_to_sleep =  2 
    for i in range(2, 50):
        base_button_xpath = '/html/body/div[4]/div/div/div[2]/ul/div'
        try:
            try:
                driver.find_element_by_xpath(f"{base_button_xpath}/li[{i}]/div/div[2]")
                xpath_for_button = f"{base_button_xpath}/li[{i}]/div/div[2]"
            except:
                xpath_for_button = f"{base_button_xpath}/li[{i}]/div/div[3]"
            if driver.find_element_by_xpath(xpath_for_button).text.lower() == 'follow':
                
                driver.find_element_by_xpath(xpath_for_button).click()
                time.sleep(time_to_sleep)
            if driver.find_element_by_xpath(xpath_for_button).text.lower() == 'follow':
                break
        except:
            logging.error("Can not find the follow users")


def open_folloowers():
    ## Function is responsible to open the followers
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
    except:
        return None



def get_followers():
    total_user = []
    for user_item in range(0, 10):
        try:
            found_user = driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{user_item}]").text.split('\n')[0]
            total_user.append(found_user)
        except:
            print(f"Was not able get user item {user_item}")
    return total_user


def save_to_file(data):
    with open('output.json', 'w') as file: 
        json.dump(data, file, indent=2)


def main():

    instagram_login()

    for username in base_users:
        driver.get(f"{base_url}/{username}")
        open_folloowers()

        for user in get_followers():
            user.append(base_users)

        save_to_file(base_users)
        follow_all()



    
if __name__ == '__main__':
    main()