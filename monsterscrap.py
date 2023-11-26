# scrape_utils.py
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def initialise_driver():
    options=webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",]
    options.add_argument(f"user-agent={user_agents}")
    # initialize driver
    driver=webdriver.Chrome(options=options)
    return driver
def scrape_website(url):
    driver=initialise_driver()
    count=0
    while(count<3):
        try:
            count=count+1
            driver.get(url+"1")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_jlc__main__VdwtF')))

            html=driver.page_source
        except:
            print("didn't connect")
        else:
            jresult={}
            count=3
            soup=BeautifulSoup(html,'html.parser')
            #data list
            dates=[]
            desc=[]
            title=[]
            exp=[]
            tages=[]
            location=[]
            salary=[]
            company=[]
            jobs=soup.find_all('div',class_='cust-job-tuple layout-wrapper lay-2 sjw__tuple')
            # traverse each job one by one
            for jb in jobs:
                #  job title
                tit=jb.find('a',class_='title').text
                title.append(tit)
                # company
                comp=jb.find_all('a')[0].text
                company.append(comp)
                # experience
                exper=jb.find('span',class_='expwdth').text
                exp.append(exper)
                # salary
                sal=jb.find('span',class_='ni-job-tuple-icon ni-job-tuple-icon-srp-rupee sal').text
                salary.append(sal)
                # location
                l=jb.find('span',class_='ni-job-tuple-icon ni-job-tuple-icon-srp-location loc').text
                location.append(l)
                # description
                de=jb.find('span',class_='job-desc ni-job-tuple-icon ni-job-tuple-icon-srp-description').text
                desc.append(de)
                # list of tags
                tags=jb.find_all('li',class_='dot-gt tag-li')
                for tt in tags:
                    tages.append(tt.text)
                #date of post
                dat=jb.find('span',class_='job-post-day').text
                dates.append(dat)
            
            #convert it into json
            jresult={"Date": dates,
                "Description": desc,
                "Title": title,
                "Experience": exp,
                "Tags":tages,
                "Location":location,
                "Salary": salary,
                "Company":company}
            return jresult


