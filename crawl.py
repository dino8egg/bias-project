import requests
from bs4 import BeautifulSoup
import pandas as pd

def log_on_text(string):
    f = open('log.txt', 'w')
    f.write(string + '\n')
    f.close()

_columns = ['conference_year', 'category', 'title', 'author', 'institution', 'abstract', 'download_url', 'pdf_file_path', 'keywords', 'publish_date']

def collect_2019():
    None
    

def collect_2018_to_2010():
    years = [18, 17, 16, 16, 14, 13, 12, 11, 10]
    webpage_url = "https://aaai.org/Library/AAAI/aaai%scontents.php"
    for year in years:
        log_on_text(str(2000+year))
        df = pd.DataFrame([], columns=_columns)
        paper_year = 2000 + year # <---------------- year
        req = requests.get(webpage_url%str(year))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        paper_url_list = soup.select('body')[0].select('#content')[0].select('#right')[0].select('#box6')[0].find('div', {'class': 'content'}).findAll('p', {'class': 'left'})
        for paper_url in paper_url_list:
            try:
                paper = paper_url.find('a').get('href').replace('view', 'viewPaper')

                if paper[-4:] == '.pdf':
                    continue

                paper_req = requests.get(paper)
                paper_html = paper_req.text
                paper_soup = BeautifulSoup(paper_html, 'html.parser')
                #print(paper)
                paper_info = paper_soup.select('body')[0].select('#container')[0].select('#body')[0].select('#main')[0]
                paper_details = paper_info.find('div',{'id': 'content'})

                paper_category = paper_info.find('div',{'id': 'breadcrumb'}).findAll('a')[3].text # <---------------- category
                paper_title = paper_details.find('div',{'id': 'title'}).text # <--------------------------------- title
                paper_author = paper_details.find('div',{'id': 'author'}).text # <---------------- author
                paper_abstract = paper_details.find('div',{'id': 'abstract'}).find('div').text # <---------------- abstract
                paper_keyword = paper_details.find('div',{'id': 'paperSubject'})  # <---------------- title
                if paper_keyword == None:
                    paper_keyword = ""
                else:
                    paper_keyword = paper_keyword.find('div').text
                paper_download_path = paper_details.find('div',{'id': 'paper'}).find('a').get('href').replace('view', 'viewFile')
                                                    # <----------------  download_path
                df = df.append(pd.DataFrame([[paper_year, paper_category, paper_title, paper_author, '', paper_abstract, paper_download_path, '', paper_keyword, '']], columns=_columns))

                # remove break
                # break
            except:
                log_on_text("error "+str(2000+year))
        df.to_csv('papers/aaai_paper_%s'%str(paper_year))
        #remove break
        #break

def get_dir_path(url):
    cnt = 1
    while url[-cnt]!='/':
        cnt = cnt + 1
    return url[:-cnt+1]

def collect_2008_to_1980():
    years = [2008, 2007, 2006, 2005, 2004, 2002, 2000, 1999, 1998, 1997, 1996, 1994, 1993, 1992, 1991, 1990, 1988, 1987, 1986, 1984, 1983, 1982, 1980]
    webpage_url = "https://aaai.org/Library/AAAI/aaai%scontents.php"
    for year in years:
        df = pd.DataFrame([], columns=_columns)
        paper_year = year # <---------------- year
        log_on_text(str(year))
        req = requests.get(webpage_url%(str(year%100)).zfill(2))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        html_tag_list = soup.find('body').select('#content')[0].select('#right')[0].select('#box6')[0].find('div', {'class': 'content'}).findAll(['p', 'h3', 'h4'])
        paper_category = ""
        for x in html_tag_list:
            try:
                if x.name == 'p' and x.has_attr('class') and paper_category != "":
                    if x == html_tag_list[-1] and (x.text.find('Index') != -1 or x.text.find('index') != -1):
                        continue

                    paper_tmp = x.find('a')
                    if paper_tmp == None:
                        continue
                    else:
                        paper_tmp = paper_tmp.get('href')
                    paper = get_dir_path(webpage_url%(str(year%100)).zfill(2)) + paper_tmp

                    if paper[-4:] == '.pdf':
                        continue

                    paper_req = requests.get(paper)
                    paper_html = paper_req.text
                    paper_soup = BeautifulSoup(paper_html, 'html.parser')
                    if paper_soup.find('body') == None:
                        paper_title = paper_soup.find('h1').text # <---------------- title
                        paper_info = paper_soup.findAll('p')
                        paper_author = paper_info[0].text # <---------------- author
                        paper_abstract = paper_info[1].text # <---------------- abstract
                        paper_info = paper_info[2:]
                        paper_keyword = ""
                        for info in paper_info:
                            if info.text.find('Subject') != -1:
                                paper_keyword = info.text # <------------- paper_keyword
                        paper_download_path = get_dir_path(paper)+paper_soup.find('h1').find('a').get('href') # <----------- path
                    else:
                        paper_info = paper_soup.find('body').find('div')
                        paper_title = paper_info.find('h1').text # <---------------- title
                        paper_info = paper_info.findAll('p')
                        paper_author = paper_info[0].text # <---------------- author
                        paper_abstract = paper_info[1].text # <---------------- abstract
                        paper_info = paper_info[2:]
                        paper_keyword = ""
                        for info in paper_info:
                            if info.text.find('Subject') != -1:
                                paper_keyword = info.text # <------------- paper_keyword
                        paper_download_path = get_dir_path(paper)+paper_soup.find('h1').find('a').get('href') # <----------- path
                    #remove break
                    #break
                    df = df.append(pd.DataFrame([[paper_year, paper_category, paper_title, paper_author, '', paper_abstract, paper_download_path, '', paper_keyword, '']], columns=_columns))


                elif x.name == 'h3' or x.name == 'h4':
                    paper_category = x.text # <---------------- category
            except:
                log_on_text("error "+str(year))
        #remove break
        df.to_csv('papers/aaai_paper_%s'%str(paper_year))
        #break

collect_2018_to_2010()
collect_2008_to_1980()