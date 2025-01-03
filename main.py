from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

with open('datas.txt', 'r') as file:
    names_and_phones = [line.strip().split(',') for line in file]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

def vote(name, phone):
    driver.execute_script("window.open('https://blacksheepindia.com/voting/', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    
    wait = WebDriverWait(driver, 10)
    captcha_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mb-3")))
    captcha_text = captcha_element.text.split()
    num1 = int(captcha_text[5])
    num2 = int(captcha_text[7].split("?")[0])
    captcha = num1 + num2

    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "phone").send_keys(phone)
    captcha_box = driver.find_element(By.ID, "captcha")
    captcha_box.send_keys(captcha, Keys.RETURN)

    vote_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/div/div/div[3]/div/a/h3')))
    vote_now_button.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    paths = [
        '/html/body/div/main/div[2]/form/div[1]/div/div[2]/label/input',
        '/html/body/div/main/div[2]/form/div[2]/div/div[11]/label/input',
        '/html/body/div/main/div[2]/form/div[20]/div/div[5]/label/input',
        '/html/body/div/main/div[2]/form/div[29]/div/div[7]/label/input',
        '/html/body/div/main/div[2]/form/div[34]/div/div[2]/label/input',
        '/html/body/div/main/div[2]/form/div[33]/div/div[2]/label/input'
    ]

    for path in paths:
        wait.until(EC.element_to_be_clickable((By.XPATH, path)))
        radio_button = driver.find_element(By.XPATH, path)
        driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
        driver.execute_script("arguments[0].click();", radio_button)
        time.sleep(1.5)

    submit_votes_button = wait.until(EC.element_to_be_clickable((By.ID, "submitVotes")))
    submit_votes_button.click()

    print(f"Form submitted. Captcha solved: {num1} + {num2} = {captcha}")
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

for name, phone in names_and_phones:
    vote(name, phone)
    time.sleep(3)

driver.quit()  
