from bs4 import BeautifulSoup
import requests
import re
import pandas as pd




def get_title(url_list):
    job_position = []
    for i in range(len(url_list)):
        response = requests.get(url_list[i])
        soup = BeautifulSoup(response.text,'html.parser')
        html = soup.find_all('div')
        req = soup.select('div h2[itemprop="name"]')
        titles = [r.text for r in req]
        titles1 = [t.replace("|","") for t in titles]
        titles = [t.replace("  ", "") for t in titles1]
        job_position = job_position + titles
    return job_position

def get_companies(url_list):
    company_name = []
    for i in range(len(url_list)):
        response = requests.get(url_list[i])
        soup = BeautifulSoup(response.text,'html.parser')
        orgs = soup.find_all('div', class_='jobCard_jobCard_cName__mYnow')
        orgs1 = [o.text for o in orgs]
        sub_str = "Hiring"
        companies = [o.split(sub_str)[0] for o in orgs1]
        company_name = company_name + companies
    return company_name


def get_cities(url_list):
    city_name = []
    pattern  = r'[0-9]'
    #strpattern = r'[a-z]'
    for i in range(len(url_list)):
        response = requests.get(url_list[i])
        soup = BeautifulSoup(response.text,'html.parser')
        loc = soup.find_all('div', class_='jobCard_jobCard_lists__fdnsc')
        loc1 = [l.div.text for l in loc]
        loc2 = [l.replace("+", ",") for l in loc1]
        location = [re.sub(pattern, '', l) for l in loc2]
        city_name = city_name + location
    return city_name

def get_experience(url_list):
    exp = []
    for i in range(len(url_list)):
        response = requests.get(url_list[i])
        soup = BeautifulSoup(response.text,'html.parser')
        loc = soup.find_all('div', class_='jobCard_jobCard_lists__fdnsc')
        experience = [l.find_all('div')[-1].text for l in loc]
        exp = exp + experience
    return exp



def get_working_mode(url_list):
    working_mode = []
    for i in range(len(url_list)):
        response = requests.get(url_list[i])
        soup = BeautifulSoup(response.text,'html.parser')
        vacancies = soup.find_all('ul', class_='jobCard_jobCard_jobDetail__jD82J')
        vac = [v.text.split("Positions") for v in vacancies ]
        working_mode = working_mode + vac
     
    
       #clean the mode
    new_working = []
    for i in range(len(working_mode)):
        tmp = working_mode[i][0]
        print(tmp)
        remove_number_tmp = tmp.rstrip('0123456789')
        new_working.append(remove_number_tmp)

    return new_working


def get_publish_date(url_list):
    publish_data =[]
    stat = []
    for i in range(len(url_list)):
        response = requests.get(url_list[i])
        soup = BeautifulSoup(response.text,'html.parser')
        date = soup.find_all('div', class_="jobCard_jobCard_features__wJid6")
        d = [l.text for l in date]
        status = [(re.sub(r'(\d+)', '\n\\1',i)).split('\n')[0] for i in d]
        d = [(re.sub(r'(\d+)', '\n\\1',i)).split('\n')[1] for i in d]
        publish_data = publish_data + d
        stat = stat + status
    return publish_data, stat



if __name__ == "__main__":
    # get url
    url_list =[]
    #tmp_url = 'https://www.shine.com/job-search/data-scientist-jobs-1?top_companies_boost=true&q=data%20scientist'
    for i in range(1,200):
        tmp = 'https://www.shine.com/job-search/data-scienst-jobs-'+str(i)+'?top_companies_boost=true&q=data%20scienst'
        url_list.append(tmp)

    # new dataframe
    df = pd.DataFrame()
    # get title
    df['Title']= get_title(url_list)
    df['Company']= get_companies(url_list)
    df['City'] = get_cities(url_list)
    df['Experience'] = get_experience(url_list)
    df['working_mode'] = get_working_mode(url_list)
    publish_date, stat = get_publish_date(url_list)
    df['Publish'] = publish_date
    df['status'] = stat
    print(df)
    df.to_csv('./data/data_scienst_shine.csv')
