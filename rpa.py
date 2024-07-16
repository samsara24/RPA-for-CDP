import os
import time
import random
import csv
import pandas as pd
import pyperclip
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from temporary import generate_random_email, get_authorization_token, fetch_verification_code

# Configuration constants
def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    config_dict = {
        "EDGE_DRIVER_PATH": config.get("Settings", "EDGE_DRIVER_PATH"),
        "URL": config.get("Settings", "URL"),
        "CSV_FILE_PATH": config.get("Settings", "CSV_FILE_PATH"),
        "OUTPUT_DIR": config.get("Settings", "OUTPUT_DIR"),
        "NOT_FOUND_FILE": config.get("Settings", "NOT_FOUND_FILE"),
        "SECRET_PASSWORD": config.get("Settings", "SECRET_PASSWORD")
    }
    
    globals().update(config_dict)

def init_driver():
    """
    Initialize the Edge WebDriver with specified options.
    """
    edge_options = Options()
    # edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # edge_options.add_argument("--no-sandbox")
    # edge_options.add_argument("--headless")  # Uncomment to run in headless mode
    service = Service(EDGE_DRIVER_PATH)
    return webdriver.Edge(service=service, options=edge_options)

def wait_and_click(driver, xpath, wait_time=5):
    """
    Wait for an element to be clickable and then click it.
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
    except TimeoutException:
        return

def register_account(driver, email, secret_password):
    """
    Register a new account using a randomly generated email and a secret password.
    """
    wait_and_click(driver, '//*[@id="createAccount"]')
    email_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))
    )
    email_input.clear()
    email_input.send_keys(email)

    wait_and_click(driver, '//*[@id="emailVerificationControl_but_send_code"]')
    time.sleep(14)

    token = get_authorization_token()
    verification_code = fetch_verification_code(email, token)
    code_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="emailVerificationCode"]'))
    )
    code_input.clear()
    code_input.send_keys(verification_code)

    wait_and_click(driver, '//*[@id="emailVerificationControl_but_verify_code"]')
    time.sleep(2 + random.random())

    password_inputs = [
        '//*[@id="newPassword"]',
        '//*[@id="reenterPassword"]'
    ]
    for xpath in password_inputs:
        secret_input = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        secret_input.clear()
        secret_input.send_keys(secret_password)

    given_name_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="givenName"]'))
    )
    given_name_input.clear()
    given_name_input.send_keys("Zien")

    surname_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="surname"]'))
    )
    surname_input.clear()
    surname_input.send_keys("Chu")

    wait_and_click(driver, '//*[@id="extension_TermsAcceptance_true"]')
    wait_and_click(driver, '//*[@id="continue"]')

def process_companies(driver, companies, times):
    """
    Process the given list of companies and save their data to text files.
    """
    for _ in range(times):
        if not companies:
            break

        company_name = companies.pop()
        query_input = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="queries_name"]'))
        )
        query_input.clear()
        query_input.send_keys(company_name)

        if times == 20:
            wait_and_click(driver, '//*[@id="onetrust-accept-btn-handler"]')
            wait_and_click(driver, '//*[@id="navobile_content"]/div[2]/div[1]/div/form/div[2]/div[2]/div[1]')
            wait_and_click(driver, '//*[@id="filters_years_chosen"]/div/ul/li[14]')

        wait_and_click(driver, '//*[@id="navobile_content"]/div[2]/div[1]/div/form/div[3]/input')
        time.sleep(3.5)

        try:
            wait_and_click(driver, '//*[@id="navobile_content"]/div[2]/div[2]/section[3]/div/table/tbody/tr[2]/td[2]/a')
        except TimeoutException:
            with open(NOT_FOUND_FILE, 'a', encoding="utf-8") as file:
                file.write(company_name + '\n')
            continue

        time.sleep(11 + random.random())
        driver.switch_to.window(driver.window_handles[-1])
        try:
            element = driver.find_element(By.XPATH, '//*[@id="formatted_responses_ndp__container"]/h1')
            element.click()
        except NoSuchElementException:
            with open(NOT_FOUND_FILE, 'a', encoding="utf-8") as file:
                file.write(company_name + '\n')
            continue
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

        page_source = pyperclip.paste()
        new_file_path = os.path.join(OUTPUT_DIR, f"{company_name}.txt")
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(page_source)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(random.random())

def main():
    """
    Main function to run the script.
    """
    load_config("config.ini")
    driver = init_driver()
    driver.get(URL)

    time.sleep(3 + random.random())
    wait_and_click(driver, '//*[@id="onetrust-accept-btn-handler"]') # cookies accept
    wait_and_click(driver, '//*[@id="regional_selection_modal"]/div/div/div[2]/ul[2]/li[2]/a') # region select

    time.sleep(3)
    wait_and_click(driver, '//*[@id="navobile_content"]/header/div[2]/nav[1]/a[4]') # sign in
    time.sleep(3 + random.random())

    email = generate_random_email() # use random email
    register_account(driver, email, SECRET_PASSWORD) # (third party service,check https://mail.cx/zh/)

    driver.get('https://www.cdp.net/en/responses?queries%5Bname%5D=Apple')
    
    # Read companies from CSV file 
    company_list = []
    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for i, row in enumerate(csvreader):
            if i < 20:
                company_list.append(row['Longname'])
    
    # Remove processed companies from CSV file
    df = pd.read_csv(CSV_FILE_PATH)
    index_to_drop = df[df['Longname'].isin(company_list)].index
    df_dropped = df.drop(index_to_drop)
    df_dropped.to_csv(CSV_FILE_PATH, index=False)

    process_companies(driver, company_list, 20)
    driver.quit()

if __name__ == "__main__":
    main()
