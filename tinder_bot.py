from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from login_details import email, password

chrome_options = Options()

chrome_options.add_argument("--remote-debugging-port=9515")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
chrome_options.add_argument("--no-sandbox"); # Bypass OS security model
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://google.com");

# chrome_options.add_argument("--no-sandbox");
# chrome_options.add_argument("--disable-dev-shm-usage");

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)

    def open_tinder(self):
        self.driver.get('https://tinder.com')
        sleep(2)
        login = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
        login.click()
        sleep(2)
        fb_login = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div[1]/div/div/div[3]/span/div[2]/button/div[2]/div[2]')
        fb_login.click()
        sleep(2)
        self.fb_popup()

    def fb_popup(self):
        #save references to main and FB windows
        base_window = self.driver.window_handles[0]
        fb_popup_window = self.driver.window_handles[1]
        #switch to FB window
        self.driver.switch_to.window(fb_popup_window)

        #find and enter email, password, login
        cookies_accept = self.driver.find_element('xpath', '/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[1]')
        cookies_accept.click()
        sleep(1)
        email_field = self.driver.find_element('xpath','/html/body/div/div[2]/div[1]/form/div/div[1]/div/input')
        password_field = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
        login_button = self.driver.find_element('xpath', '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input')
        #enter info
        email_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()
        try:
            self.driver.switch_to.window(base_window)
        except:
            print('failed to attach to:', base_window)
        
        sleep(6)
        try:
            allow_btn = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[1]')
            allow_btn.click() 
        except:
            print('no allow') 
        
# bot = TinderBot()
# bot.open_tinder()