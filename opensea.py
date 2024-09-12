import os
import time
from dotenv import load_dotenv
import logging
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

price="0.003"
numOfNFTs = 100
offset = 1385
url = "https://testnets.opensea.io/assets/goerli/0x1f419b9469d641d333805c4054ca3b65af54d315"

EXTENSION_PATH = os.getcwd() + "/extension_10_22_1_0.crx"
chrome_driver = os.getcwd() + "/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_extension(EXTENSION_PATH)
driver = webdriver.Chrome(options=chrome_options,executable_path=chrome_driver)

class SetForSaleOnOpensea(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.SECRET_WORDS = os.getenv('SECRET_WORDS')
        self.PASSWORD = os.getenv('PASSWORD')

        if self.SECRET_WORDS == "" or self.SECRET_WORDS == None:
            driver.quit()
            raise Exception('Secret phrase not defined. Please provide wallet secret phrase as one string in .env file')
        if self.PASSWORD == "" or self.PASSWORD == None:
            driver.quit()
            raise Exception('Password not defined. Please provide password in the .env file')

        driver.get("https://testnets.opensea.io/collection/snakes-on-a-chain-goerli")
        if not "OpenSea" in driver.title:
            raise Exception("Unable to load page!")

    def typeSecretWords(self, secretWords):
        listOfSecretWords = secretWords.split()

        for i in range(len(listOfSecretWords)):
            driver.find_element(By.XPATH, f'//*[@id="import-srp__srp-word-{i}"]').send_keys(listOfSecretWords[i])


    def setForSale(self, chld, parent):
        for i in range(numOfNFTs):
            driver.get(url + '/' + str(i + offset) + '/sell')
            time.sleep(3)

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'price')))
                driver.find_element(By.ID, "price").send_keys(price)
                driver.find_element(By.XPATH, "//*[contains(text(), 'Complete listing')]").click()
                time.sleep(3)
                driver.switch_to.window(chld)
                driver.refresh()

                # Seapport - arrow
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div[1]/i')))
                driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div[1]/i').click()

                # Sign btn
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[4]/button[2]')))
                driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[4]/button[2]').click()

                # Switch to OpenSea tab
                driver.switch_to.window(parent)
                time.sleep(3)

            except Exception as e:
                logging.error('error setting for sale', exc_info=e)

    def test_SetForSaleOnOpensea(self):
        parent = driver.window_handles[1]
        # print(driver.title)
        chld = driver.window_handles[0]
        # print(driver.title)
        driver.switch_to.window(chld)
        # print(driver.title)
        driver.close()
        driver.switch_to.window(parent)

        #  Wallet button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="__next"]/div/div[1]/div/nav/ul/div[2]/div/div[2]/li/div/button')))
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div/nav/ul/div[2]/div/div[2]/li/div/button').click()
        time.sleep(0.5)
        # Metamask Logo
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="__next"]/div/aside[2]/div[2]/div/div[2]/ul/li[1]/button')))
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/aside[2]/div[2]/div/div[2]/ul/li[1]/button').click()

        time.sleep(3)

        parent = driver.window_handles[0]
        chld = driver.window_handles[1]
        driver.switch_to.window(chld)

        time.sleep(3)

        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[1]').click()
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button').click()

        self.typeSecretWords(self.SECRET_WORDS)

        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('12345678')
        driver.find_element(By.XPATH, '//*[@id="confirm-password"]').send_keys('12345678')

        driver.find_element(By.XPATH, '//*[@id="create-new-vault__terms-checkbox"]').click()
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button').click()


        # All done
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="app-content"]/div/div[2]/div/div/button')))
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/button').click()

        # Network
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div/div').click()
        # Show/hide testnets
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="app-content"]/div/div[2]/div/div[1]/div[3]/span/a')))

        button = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[1]/div[3]/span/a')
        driver.execute_script("arguments[0].click();", button)
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[8]/div[2]/div/label/div[1]').click()
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div/div').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/li[2]').click()
        #  Close Metamask settings
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[1]/div[1]/div[2]').click()

        driver.switch_to.window(parent)

        # Metamask Logo
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="__next"]/div/aside[2]/div[2]/div/div[2]/ul/li[1]/button')))
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/aside[2]/div[2]/div/div[2]/ul/li[1]/button').click()

        driver.switch_to.window(chld)
        driver.refresh()
        #  Next btn
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]')))
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]').click()

        # Connect btn
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
            '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]')))
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()

        driver.switch_to.window(parent)
        # Go to profile page
        #WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
        #    '//*[@id="__next"]/div/div[1]/div/nav/ul/div[2]/div/div[1]/li/a/span/img')))
        #driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div/nav/ul/div[2]/div/div[1]/li/a/span/img').click()
        #time.sleep(3)

        self.setForSale(chld, parent)

    def tearDown(self):
        driver.quit()

if __name__ == '__main__':
    unittest.main()