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

numOfNFTs = 999
offset = 1037
url = "https://testnets.opensea.io/assets/goerli/0x1f419b9469d641d333805c4054ca3b65af54d315"

EXTENSION_PATH = os.getcwd() + "/extension_10_22_1_0.crx"
chrome_driver = os.getcwd() + "/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
#chrome_options.add_extension(EXTENSION_PATH)
driver = webdriver.Chrome(options=chrome_options,executable_path=chrome_driver)

class SetForSaleOnOpensea(unittest.TestCase):
    def setUp(self):
        driver.get("about:blank")


    def setForSale(self):
        for i in range(numOfNFTs):
            driver.get(url + '/' + str(i + offset))
            time.sleep(1)

            try:
                driver.find_element(By.CSS_SELECTOR, "button[aria-label=More]").click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, ".tippy-box li:first-child>button").click()
                time.sleep(2)

            except Exception as e:
                logging.error('error setting for sale', exc_info=e)

    def test_SetForSaleOnOpensea(self):
        self.setForSale()

    def tearDown(self):
        driver.quit()

if __name__ == '__main__':
    unittest.main()