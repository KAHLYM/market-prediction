import logging
import json
import os
from pathlib import Path
import time
from typing import List
import urllib

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_sp500(path: str) -> List:
    with open(path) as f:
        return json.load(f)

TICKER_LIST = get_sp500('../s&p500/s&p500.json')
OUTPUT_DIRECTORY = os.path.join(str(Path(__file__).parent.absolute()), 'output')

Path(OUTPUT_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Logging
logging_level = logging.DEBUG
logger = logging.getLogger('logos')
logger.setLevel(logging_level)
ch = logging.StreamHandler()
ch.setLevel(logging_level)
formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Install Chrome webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Accept Google cookies
driver.get('https://www.google.com/search?q=test')
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src, 'consent.google.com')]"))
page_wait_cookies = 5
logger.info(f'Waiting { page_wait_cookies } second for page load to accept cookies ...')
time.sleep(page_wait_cookies)
driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span').click()

complete = []

for ticker in TICKER_LIST:

    logo_path = os.path.join(OUTPUT_DIRECTORY, ticker + '.jpg')

    # Check if ticker already complete
    if (ticker in complete) or (os.path.exists(logo_path)):
        logger.debug(f'Already completed { ticker }. Continuing.')
        continue
    
    page_wait_ticker = 0.5

    max_attempt = 3
    for attempt in range(1, max_attempt + 1):
        try:
            # Retrieve Google search query
            url = f'https://www.google.com/search?q={ ticker }+stock'
            driver.get(url)
            logger.debug(f'Waiting { page_wait_ticker } second for page load ...')
            time.sleep(page_wait_ticker)

            try:
                # Check if reCAPTCHA triggered
                about_this_page = driver.find_element_by_xpath('/html/body/div/div/b').get_attribute('innerHTML')
                if (about_this_page == 'About this page'):
                    logger.info(f'reCAPTCHA triggered. Saving checkpoint. Restarting driver.')
                    
                    # Kill Chrome webdriver
                    driver.quit()

                    # Install Chrome webdriver
                    driver = webdriver.Chrome(ChromeDriverManager().install())

                    # Accept Google cookies
                    driver.get('https://www.google.com/search?q=test')
                    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src, 'consent.google.com')]"))
                    page_wait_cookies = 5
                    logger.info(f'Waiting { page_wait_cookies } second for page load to accept cookies ...')
                    time.sleep(page_wait_cookies)
                    driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span').click()
            except:
                pass

            # Extract image source
            logo_src = driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[9]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div/a/g-img/img').get_attribute('src')

            # Download image source
            logger.debug(f'Downloading { ticker } image source ...')
            urllib.request.urlretrieve(logo_src, logo_path)
            complete.append(ticker)
            break

        except Exception as e:
            # Check if final attempt
            if attempt == max_attempt:
                logger.error(f"Failed { ticker }")
                logger.error(e)
                complete.append(ticker)

            # Increase wait
            page_wait_ticker = page_wait_ticker * attempt + 1
            continue

driver.quit()
