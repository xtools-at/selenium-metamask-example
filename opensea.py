import os
import time
from dotenv import load_dotenv
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        driver.get("https://testnets.opensea.io/")
        if not "OpenSea" in driver.title:
            raise Exception("Unable to load google page!")
    
    def typeSecretWords(self, secretWords):
        listOfSecretWords = secretWords.split()

        for i in range(len(listOfSecretWords)):
            driver.find_element(By.XPATH, f'//*[@id="import-srp__srp-word-{i}"]').send_keys(listOfSecretWords[i])

    
    def setForSale(self, chld, parent):
        numOfNFTs = len(driver.find_elements(By.TAG_NAME, "article"))
        print(f"Number of total NFTs detected: {numOfNFTs}")

        for i in range(numOfNFTs):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
            NFT = driver.find_elements(By.TAG_NAME, "article")[i]
            NFT_ID = NFT.find_element(By.TAG_NAME, "img").get_attribute("alt")
            print(f'Trying to list NFT: {NFT_ID}')
            NFT.click()
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, "//*[contains(text(), 'Sell')]").click()

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'price')))
                driver.find_element(By.ID, "price").send_keys("0.001")
                driver.find_element(By.XPATH, "//*[contains(text(), 'Complete listing')]").click()
                time.sleep(3)
                driver.switch_to.window(chld)
                driver.refresh()

                # Seapport - arrow
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'i[title="Scroll down"]')))
                driver.find_element(By.CSS_SELECTOR, 'i[title="Scroll down"]').click()

                # Sign btn
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="signature-sign-button"]')))
                driver.find_element(By.CSS_SELECTOR, 'button[data-testid="signature-sign-button"]').click()

                # Switch to OpenSea tab
                driver.switch_to.window(parent)
                time.sleep(1)

                # Close modal
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'i[aria-label="Close"]')))
                driver.find_element(By.CSS_SELECTOR, 'i[aria-label="Close"]').click()
            except: print(f'Sell button not present for NFT: {NFT_ID}')

            # Go to profile page
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                'img[alt="Account"]')))
            try:
                driver.find_element(By.CSS_SELECTOR, 'img[alt="Account"]').click()
            except: print('button not found')
            time.sleep(3)

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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
            'i[title="Wallet"]')))
        driver.find_element(By.CSS_SELECTOR, 'i[title="Wallet"]').click()
        time.sleep(0.5)
        # Metamask Logo
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            "//*[contains(text(), 'MetaMask')]")))
        driver.find_element(By.XPATH, "//*[contains(text(), 'MetaMask')]").click()

        time.sleep(5)

        parent = driver.window_handles[0]
        chld = driver.window_handles[1]
        driver.switch_to.window(chld)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
            '[data-testid="first-time-flow__button"]')))
        driver.find_element(By.CSS_SELECTOR, '[data-testid="first-time-flow__button"]').click()
        driver.find_element(By.CSS_SELECTOR, '[data-testid="page-container-footer-cancel"]').click()
        driver.find_element(By.CSS_SELECTOR, '[data-testid="import-wallet-button"]').click()

        self.typeSecretWords(self.SECRET_WORDS)

        driver.find_element(By.ID, 'password').send_keys('12345678')
        driver.find_element(By.ID, 'confirm-password').send_keys('12345678')

        driver.find_element(By.ID, 'create-new-vault__terms-checkbox').click()
        driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        # All done
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
            '[data-testid="EOF-complete-button"]')))
        driver.find_element(By.CSS_SELECTOR, '[data-testid="EOF-complete-button"]').click()

        # Network
        driver.find_element(By.CSS_SELECTOR, '[data-testid="network-display"]').click()
        # Show/hide testnets
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            "//*[contains(text(), 'Show/hide')]")))
        button = driver.find_element(By.XPATH, "//*[contains(text(), 'Show/hide')]")
        driver.execute_script("arguments[0].click();", button)

        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[8]/div[2]/div/label/div[1]').click()
        driver.find_element(By.CSS_SELECTOR, '[data-testid="network-display"]').click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '[data-testid="goerli-network-item"]').click()
        #  Close Metamask settings
        driver.find_element(By.CSS_SELECTOR, '[class="settings-page__header__title-container__close-button"]').click()
        
        driver.switch_to.window(parent)

        # Metamask Logo
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            "//*[contains(text(), 'MetaMask')]")))
        driver.find_element(By.XPATH, "//*[contains(text(), 'MetaMask')]").click()

        driver.switch_to.window(chld)
        driver.refresh()
        #  Next btn
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
            "//*[contains(text(), 'Next')]")))
        driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]").click()

        # Connect btn
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR,
            '[data-testid="page-container-footer-next"]')))
        driver.find_element(By.CSS_SELECTOR, '[data-testid="page-container-footer-next"]').click()
        
        driver.switch_to.window(parent)
        # Go to profile page
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                'img[alt="Account"]')))
        driver.find_element(By.CSS_SELECTOR, 'img[alt="Account"]').click()
        time.sleep(3)
        
        self.setForSale(chld, parent)

    
    def tearDown(self):
        driver.quit()

if __name__ == '__main__':
    unittest.main()