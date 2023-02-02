from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from login_details import people
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_argument("--remote-debugging-port=9515")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--incognito");
chrome_options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
chrome_options.add_argument("--no-sandbox"); # Bypass OS security model

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def close_down(self):
        self.driver.close()

    def open_tinder(self, email, password):
        self.driver.get('https://tinder.com')

        sleep(2)

        login = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
        login.click()
        sleep(1)
        self.facebook_login(email, password)

        sleep(6)
        # try:
        #     allow_location_button = self.driver.find_element('xpath', '//*[@id="t-1917074667"]/main/div/div/div/div[3]/button[1]')
        #     allow_location_button.click()
        # except:
        #     print('no location popup')
        # sleep(1)
        try:
            notifications_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
            notifications_button.click()
        except:
            print('no notification popup')
        sleep(1)
        try:
            meet_people_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[1]/div[2]/div[2]')
            meet_people_button.click()
        except:
            print('no meet people popup')
        sleep(1)
        try:
            no_not_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
            no_not_button.click()
        except:
            print('no no notifications popup')
    
    def facebook_login(self, email, password):
        # find and click FB login button
        # login_with_facebook = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div[1]/div/div/div[3]/span/div[2]/button')
        login_with_facebook = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button/div[2]/div[2]/div/div')

        login_with_facebook.click()   
        # save references to main and FB windows
        sleep(2)
        base_window = self.driver.window_handles[0]
        fb_popup_window = self.driver.window_handles[1]
        # switch to FB window
        self.driver.switch_to.window(fb_popup_window)

        # find enter email, password, login
        cookies_accept_button = self.driver.find_element('xpath', '/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[1]')
        cookies_accept_button.click()

        # login to FB
        email_field = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[1]/div/input')
        pw_field = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
        login_button = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input')
        # enter email, password and login
        email_field.send_keys(email)
        pw_field.send_keys(password)
        login_button.click()
        self.driver.switch_to.window(base_window)

    def right_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)
    def left_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_LEFT)

    def auto_swipe(self):
        for x in range(3):
            sleep(2)
            try:
                if (x % 5 == 1):
                    self.left_swipe()
                else:
                    self.right_swipe()
                x = x-1
            except:
                self.close_match()
                x = x-1

    def close_match(self):
        match_popup = self.driver.find_element('xpath', '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def get_matches(self):
        match_profiles = self.driver.find_elements('class name', 'matchListItem')
        message_links = []
        for profile in match_profiles:
            if profile.get_attribute('href') == 'https://tinder.com/app/my-likes' or profile.get_attribute('href') == 'https://tinder.com/app/likes-you':
                continue
            message_links.append(profile.get_attribute('href'))
        return message_links

    def send_messages_to_matches(self):
        links = self.get_matches()
        for link in links:
            self.send_message(link)

    def send_message(self, link):
        self.driver.get(link)
        sleep(2)
        text_area = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea')

        text_area.send_keys('hi')

        text_area.send_keys(Keys.ENTER)

for x in range(len(people)):
    bot = TinderBot()
    bot.open_tinder(people[x]["email"], people[x]["password"])
    sleep(10)
    bot.auto_swipe()
    bot.close_down()
    sleep(2)
# bot.send_messages_to_matches()