import time
import requests
import csv
from bs4 import BeautifulSoup

AAAI_2019_URL = "https://aaai.org/Library/AAAI/aaai19contents.php"
STORED_DIR = "../../../data/AAAI_2019_papers"
TSV_DIR = "../../../data/AAAI_2019_info.tsv"

def crawl_test():
	main_page = requests.get(AAAI_2019_URL)
	soup = BeautifulSoup(main_page.text, 'html.parser')
	papers = soup.find_all("p", {"class": "left"})
	
	with open(TSV_DIR, 'wt') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		for paper in papers:
			paper_urls = paper.find_all("a")
			info_url = paper_urls[0]['href']
			pdf_url = paper_urls[1]['href']

			info_page = requests.get(info_url)
			paper_soup = BeautifulSoup(info_page.text, 'html.parser')

			paper_title = paper_soup.find("h1", {"class": "page_title"}).find(text=True)
			paper_title = ' '.join(paper_title.split())

			authors = paper_soup.find("ul", {"class": "item authors"}).find_all("li")
			paper_authorlist = []
			for author in authors:
				paper_author = {}
				author_info = author.find_all("span")
				author_name = author_info[0].find(text=True)
				author_name = ' '.join(author_name.split())
				paper_author["name"] = author_name

				author_affiliation = author_info[1].find(text=True)
				author_affiliation = ' '.join(author_name.split())
				paper_author["affiliation"] = author_affiliation
				paper_authorlist.append(paper_author)
			paper_authors = ','.join(["("+author['name']+","+author['affiliation']+")" for author in paper_authorlist])
			
			publish_info = paper_soup.find("div", {"class": "item published"})
			publish_date = publish_info.find("div", {"class": "value"}).find(text=True)
			paper_publish_date = ' '.join(publish_date.split())

			section_info = paper_soup.find("div", {"class": "item issue"}).find_all("div", {"class": "sub_item"})
			paper_section = section_info[1].find("div", {"class": "value"}).find(text=True)
			paper_section = ' '.join(paper_section.split())
			
			abstract_info = paper_soup.find("div", {"class": "item abstract"}).find_all("p")
			paper_abstract = ' '.join([abstract.text for abstract in abstract_info])
			tsv_writer.writerow(['2019', paper_section, paper_title, paper_authors, paper_abstract, pdf_url, '', paper_publish_date])


if __name__ == '__main__':
	start = time.time()
	crawl_test()
	end = time.time()
	print("Execution Time: {}".format(end-start))