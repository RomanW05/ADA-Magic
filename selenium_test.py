from selenium import webdriver    
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import random
import time



chromedriver_autoinstaller.install()




driver = webdriver.Chrome(service=Service())

def login(driver):
	# Main page
	driver.get("http://localhost:8080/login")
	time.sleep(0.1)
	# elem = driver.find_elements(By.ID, "modal_trigger")
	# elem[0].click()

	# # Login form
	# time.sleep(0.1)
	elem = driver.find_elements(By.ID, "username")
	elem[0].click()

	time.sleep(0.1)
	username = driver.find_elements(By.ID, "username")
	username[0].send_keys('claro2')

	time.sleep(0.1)
	password = driver.find_elements(By.ID, "password")
	password[0].send_keys('bbb')

	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "send_message")
	elem[0].click()


def test_double_empty_metadata_fields(driver):
	# Login
	login(driver)

	# Mint
	driver.get("http://localhost:8080/mint")
	time.sleep(0.1)

	# Fill requested fields
	elem = driver.find_elements(By.ID, "upload_file")
	elem[0].send_keys("C:/Users/yop/Desktop/astral.png")

	artist_price_title(driver)

	elem = driver.find_elements(By.ID, "submit")
	elem[0].send_keys(Keys.RETURN)


def test_single_nft(driver):
	# Login
	login(driver)

	# Mint
	driver.get("http://localhost:8080/mint")
	time.sleep(0.1)

	# Fill requested fields
	elem = driver.find_elements(By.ID, "upload_file")
	elem[0].send_keys("C:/Users/yop/Desktop/astral.png")

	artist_price_title(driver)

	# Test add more fields button
	elem = driver.find_elements(By.ID, "addMore2")
	elem[0].send_keys(Keys.RETURN)

	elem = driver.find_elements(By.ID, "submit")
	elem[0].send_keys(Keys.RETURN)



def test_metadata(driver):
	# Login
	login(driver)

	# Mint
	driver.get("http://localhost:8080/mint")
	time.sleep(0.1)

	# Fill requested fields
	elem = driver.find_elements(By.ID, "upload_file")
	elem[0].send_keys("C:/Users/yop/Desktop/astral.png")

	artist_price_title(driver)

	# Test metadata

	elem = driver.find_elements(By.ID, "metadata_0_0")
	elem[0].send_keys('metadata00')

	elem = driver.find_elements(By.ID, "metadata_0_1")
	elem[0].send_keys('metadata01')

	# Test add more fields button
	elem = driver.find_elements(By.ID, "addMore2")
	elem[0].send_keys(Keys.RETURN)
	time.sleep(0.3)


	# Fill another field


	# Select a collection
	elem = driver.find_elements(By.ID, "li_new_collection")
	time.sleep(1)
	elem[0].click()

	elem = driver.find_elements(By.ID, "collection_name_id")
	elem[0].send_keys('Collection name 1')

	elem = driver.find_elements(By.ID, "upload_file_collection")
	elem[0].send_keys("C:/Users/yop/Desktop/photo_2022-02-22_12-51-04.jpg")
	


	elem = driver.find_elements(By.ID, "submit")
	elem[0].send_keys(Keys.RETURN)









'''

CREATE TABLE `collections` (
  `internal_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `collection_name` varchar(64) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `policy_id` varchar(255) DEFAULT NULL,
  UNIQUE KEY `policy_id_UNIQUE` (`policy_id`)
);
ALTER TABLE `collections` ADD UNIQUE `unique_index`(`collection_name`, `username`);


CREATE TABLE `collections_users` (
  `internal_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` varchar(64) DEFAULT NULL,
  `single_nft_internal_id` varchar(64) DEFAULT NULL,
  `collection_id` int,
  `policy_id` varchar(255) DEFAULT NULL,
FOREIGN KEY (`collection_id`) REFERENCES `collections` (`internal_id`),
FOREIGN KEY (`policy_id`) REFERENCES `collections` (`policy_id`)
ON DELETE CASCADE ON UPDATE CASCADE
);
ALTER TABLE `collections_users` ADD UNIQUE `unique_index`(`username`, `single_nft_internal_id`);


'''


def artist_price_title(driver):
	integer = random.randint(0, 10000)
	elem = driver.find_elements(By.ID, "item_title")
	elem[0].send_keys(f'{integer}title')

	elem = driver.find_elements(By.ID, "item_price")
	elem[0].send_keys('5')

	elem = driver.find_elements(By.ID, "item_artist")
	elem[0].send_keys('mamoma')

	elem = driver.find_elements(By.ID, "item_desc")
	elem[0].send_keys("Item's description with multiple fucked up chars!, l;ike:.\n ?here we go, mate")
	
ALTER TABLE `nicehqrq_nft`.`single_nfts` 
ADD COLUMN `verified_status` INT NULL AFTER `collection_name`,
ADD INDEX `verified_status_idx` (`verified_status` ASC) VISIBLE;
;
ALTER TABLE `nicehqrq_nft`.`single_nfts` 
ADD CONSTRAINT `verified_status`
  FOREIGN KEY (`verified_status`)
  REFERENCES `nicehqrq_nft`.`users` (`verified_status`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE `single_nfts` ADD FOREIGN KEY (verified_status, username_id) REFERENCES `users` (verified_status, internal_id) ON UPDATE CASCADE;


def create_new_vending_machine_project(driver):
	layer1 = [
		
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer1/background_1.PNG",
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer1/background_2.PNG",
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer1/background_3.PNG",
	]

	layer2 = [
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer2/element_1.PNG",
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer2/element_2.PNG",
	]

	layer3 = [
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer3/skin_1.PNG",
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer3/skin_2.PNG",
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer3/skin_3.PNG",
	]

	layer4 = [
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer4/marking_1.PNG",
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer4/marking_2.PNG",
	"C:/Users/yop/Desktop/proyects/NFT/astral_sisters/layer4/marking_3.PNG",
	]


	# Main page
	driver.get("http://localhost:8080/login")
	time.sleep(0.1)
	# elem = driver.find_elements(By.ID, "modal_trigger")
	# elem[0].click()

	# # Login form
	# time.sleep(0.1)
	elem = driver.find_elements(By.ID, "username")
	elem[0].click()

	time.sleep(0.1)
	username = driver.find_elements(By.ID, "username")
	username[0].send_keys('claro2')

	time.sleep(0.1)
	password = driver.find_elements(By.ID, "password")
	password[0].send_keys('bbb')

	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "send_message")
	elem[0].click()


	# Vending machine page
	driver.get("http://localhost:8080/vending_m")
	time.sleep(0.1)

	elem = driver.find_elements(By.ID, "thumbnail_a")
	elem[0].send_keys("C:/Users/yop/Desktop/astral.png")

	elem = driver.find_elements(By.ID, "get_file_b0")
	for file in layer1:
		print(elem)
		elem[0].send_keys(file)

	elem = driver.find_elements(By.ID, "get_file_b1")
	for file in layer2:
		elem[0].send_keys(file)

	elem = driver.find_elements(By.ID, "get_file_b2")
	for file in layer3:
		elem[0].send_keys(file)

	elem = driver.find_elements(By.ID, "get_file_b3")
	for file in layer4:
		elem[0].send_keys(file)

	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "item_title")
	elem[0].send_keys('jsdafiojwer')

	elem = driver.find_elements(By.ID, "collection_total")
	elem[0].send_keys('22')

	elem = driver.find_elements(By.ID, "item_price")
	elem[0].send_keys('5')

	elem = driver.find_elements(By.ID, "item_artist")
	elem[0].send_keys('mamoma')

	elem = driver.find_elements(By.ID, "item_desc")
	elem[0].send_keys('Cool description here')

	elem = driver.find_elements(By.ID, "item_royalties")
	elem[0].send_keys('13')

	elem = driver.find_elements(By.ID, "item_website")
	elem[0].send_keys('www.https://test.html')

	
	

	elem = driver.find_elements(By.ID, "date_to_change")
	elem[0].send_keys('10-04-2018')
	elem[0].send_keys(Keys.TAB)
	elem[0].send_keys("0245PM")
	# time.sleep(0.1)

	# elem[0].submit()
	time.sleep(0.5)
	elem = driver.find_elements(By.ID, "submit")
	elem[0].click()
	elem[0].submit()
	# WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, "date_to_change"))).click()
	# WebDriverWait(driver, 4)
	# elem[0].send_keys(Keys.UP)
	# elem[0].send_keys(Keys.RIGHT)
	# elem[0].send_keys(Keys.UP)
	# elem[0].send_keys(Keys.RIGHT)
	# elem[0].send_keys(Keys.UP)
	# elem[0].send_keys(Keys.RIGHT)
	# elem[0].send_keys(Keys.UP)
	# elem[0].send_keys(Keys.RIGHT)
	# elem[0].send_keys(Keys.UP)

	# element = WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, 'submit')))
	# print(element)
	# sys.exit()
	# button = driver.find_elements(By.ID, "submit")
	# print('/n/n', button[0], '/n/n')
	# driver.execute_script("arguments[0].click();", button)

	# WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "submit"))).click()
	# WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > form:nth-child(10) > input:nth-child(3)"))).click()
	# elem = driver.find_elements(By.ID, "submit")
	# elem[0].click()

	# time.sleep(3)
	# New page
	# elem = driver.find_elements(By.ID, "yes")
	# elem[0].click()

	# Check data
	# time.sleep(600)


def create_new_user(driver):
	# Main page
	driver.get("https://adamagic.io")
	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "modal_trigger")
	elem[0].click()

	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "register_form")
	elem[0].click()

	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "username")
	elem[0].send_keys('ddsadwe')

	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "email")
	elem[0].send_keys('impactoworld43@gmail.com')
	
	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "register")
	elem[0].click()	

def seed():
	driver.get("https://adamagic.io/giga/login")
	time.sleep(0.1)
	# elem = driver.find_elements(By.ID, "modal_trigger")
	# elem[0].click()

	# # Login form
	# time.sleep(0.1)
	elem = driver.find_elements(By.ID, "username")
	elem[0].click()

	time.sleep(0.1)
	username = driver.find_elements(By.ID, "username")
	username[0].send_keys('Claro4')

	time.sleep(0.1)
	password = driver.find_elements(By.ID, "password")
	password[0].send_keys('bbb')

	time.sleep(0.1)
	elem = driver.find_elements(By.ID, "send_message")
	elem[0].click()

	driver.get("https://adamagic.io/inform_user")
	time.sleep(0.1)
	
	tags = []
	elem = driver.find_elements(By.ID, "input_tags")
	for word in tags:
		elem[0].send_keys(word)
		elem[0].send_keys(' ')
		time.sleep(0.1)

	elem = driver.find_elements(By.ID, "submit")
	elem[0].click()	
	
# create_new_vending_machine_project(driver)
# create_new_vending_machine_project(driver)
# test_metadata(driver)
# test_single_nft(driver)
test_double_empty_metadata_fields(driver)
