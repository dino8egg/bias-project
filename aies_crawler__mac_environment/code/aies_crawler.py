from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import csv
from bs4 import BeautifulSoup

TSV_DIR = "../../data/AIES_2019_info.tsv"
AIES_2019_URL = "http://www.aies-conference.com/2019/accepted-papers/"
main_page = requests.get(AIES_2019_URL)
soup = BeautifulSoup(main_page.text, 'html.parser')
papers = soup.find_all("strong")

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)
# 2018: 21 23 24
# 2019: 59 61
cnt = 0
with open(TSV_DIR, 'a') as out_file:
	tsv_writer = csv.writer(out_file, delimiter='\t')
	for paper_title in papers[62:]:
		title = paper_title.find(text=True)
		print(title)
		print(cnt)
		cnt += 1
		driver.get('https://dl.acm.org/dl.cfm')
		driver.find_element_by_name('query').send_keys(title)
		driver.find_element_by_name('Go').click()
		driver.find_element_by_xpath('//a[contains(@href, "citation.cfm")]').click()
		# driver.find_element_by_id('tab-1011-btnEl').click()
		# driver.implicitly_wait(1)
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CLASS_NAME, "tabbody"))
		)

		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		abstract = " ".join(soup.find("div", {"class": "tabbody"}).find_all(text=True)).lstrip().rstrip()
		print(abstract)
		tsv_writer.writerow(['2018', 'AIES', title, 'None', abstract, 'None', '', 'None'])
