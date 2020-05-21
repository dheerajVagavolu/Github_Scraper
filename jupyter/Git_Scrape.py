#!/usr/bin/env python
# coding: utf-8

# # Git Scrape

# ### 1) Read file

# In[156]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import csv
import time
from datetime import datetime


# In[162]:


# website urls
# base_url = "https://github.com/airbnb/epoxy/pulls?q=is%3Apr+is%3Aclosed+closed%3A2019-10-30..2020-04-30"

def load_base(base_url):
    print(base_url)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(base_url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()

    issues = soup.find_all('div', class_="flex-auto min-width-0 lh-condensed p-2 pr-3 pr-md-2")
    print(len(issues))
    return [issues, soup]


# In[163]:


def get_num(string):
    return string.strip().split(' ')[0].replace(' ','')


# In[161]:


def get_deeper(kind, href, close_date, soup):
    
    print()
    driver = webdriver.Chrome()
    driver.get(href)
    driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    
    participants = soup.find('div', class_="participation")
    participants = get_num(participants.text.strip())
    
    title = soup.find('span', class_="js-issue-title")
    title = title.text.strip()
    
    labels = soup.find('div', class_="labels")
    labels = labels.text.strip()
    
    status = soup.find('span', class_="State")
    status = status['title'].strip()
    status = status.split(' ')[-1]
    
    ## Prints
    
    print(kind,"\n---------")
    print("Title:",title)
    print("Status:",status)
    print("Labels:",labels)
    print("Participants:",participants)
    
    
    ## Files
    
    if kind == "pull":
        
        try:
            file_changed = soup.find(id="files_tab_counter")
            file_changed = file_changed.text.strip()
        except:
            file_changed = 'n/a'
        
        try:
            lines_added = soup.find('span', class_="text-green")
            lines_added = lines_added.text.strip()
            lines_added = lines_added[1:]
        except:
            lines_added = 'n/a'
        
        try:
            lines_removed = soup.find('span', class_="text-red")
            lines_removed = lines_removed.text.strip()
            lines_removed = lines_removed[1:]
        except:
            lines_removed = 'n/a'

        print("Files Changed:",file_changed)
        print("Lines Added:",lines_added)
        print("Lines Removed",lines_removed)
        print("Approved Date:",close_date)
        
        object_tuple = [title, labels,                         participants,                        close_date,                         file_changed, lines_added, lines_removed,                        status]
        
        print(object_tuple)
    
    if kind =="issue":
        
        try:
            comment_tab = soup.find('div',"TableObject-item TableObject-item--primary")
        except:
            comment_tab = 'n/a'
        
        try:
            rel_time = soup.find('relative-time')
            open_date = rel_time['datetime']
            open_date = open_date[:10]
        except:
            open_date = 'n/a'
            
        
        print("Inner_date:",open_date)
        print("Outer_date:",close_date)
        
        try:
            comments = comment_tab.text.strip().split('\n')[-1].split(' ')[1].strip()
        except:
            comments = 'n/a'
            
        print("Comments:", comments)
          
        object_tuple = [title, labels,                         participants, open_date,                        close_date,                         comments,                        status]
        
        print(object_tuple)
    
    return object_tuple
        
        


# In[160]:


def outer_page(issues, soup):
    objects = []
    for issue in issues:
            meta_data = issue.find('relative-time')
            issue_link = issue.find_all('a', class_='link-gray-dark v-align-middle no-underline h4 js-navigation-open')
            close_date = meta_data['datetime'][:10]
            for link in issue_link:
                try:
                    if 'issue' in link['id']:
                        href = link['href']
                        
                        kind = "pull"
                        if "issue" in href:
                            kind = "issue"
                        
                        href = 'https://github.com'+href
                        print("\n",href) 
                        obj = get_deeper(kind, href, close_date, soup)
                        objects.append(obj)
                except:
                    pass
    return objects

# outer_page()
# outer_page("pull")


# In[159]:


def get_name(string):
    return string.split('/')[-1].strip()


# In[171]:


def main():
    repo_list = open('list').readlines()
    range_list = [(i.split(' ')[0], i.split(' ')[1], i.split(' ')[2]) for i in repo_list]

    for i in range_list:
        base_url = i[0]
        name = get_name(base_url)
        print(name)
        print("Base_Url:", base_url)
        num_pages_issues = int(i[1])
        num_pages_pulls = int(i[2])

        print("Issues Pages:",num_pages_issues)

        dat = ['Title', 'Labels', 'Participants', 'Open_date', 'Close_date', 'Comments', 'Status']

        with open('data/'+name+'_'+"issues_2019-10-30_2020-04-30" + '.csv', 'a', newline='', encoding="utf-8") as csvfile:
                f1w = csv.writer(csvfile)
                f1w.writerow(dat)


        for num in range(num_pages_issues):
            link = "/issues?page="+str(num+1)+"&q=is%3Aissue+is%3Aclosed+closed%3A2019-10-30..2020-04-30"
            link = base_url + link
            returns = load_base(link)
            time.sleep(5)
            objects = outer_page(returns[0], returns[1])
            with open('data/'+name+'_'+"issues_2019-10-30_2020-04-30" + '.csv', 'a', newline='',encoding="utf-8") as csvfile:
                f1w = csv.writer(csvfile)
                for _obj in objects:
                    f1w.writerow(_obj)




        print("Pulls Pages:",num_pages_pulls)

        dat = ['Title', 'Labels', 'Participants', 'Approved_date', 'files_changed', 'lines_added','lines_deleted','Status']

        with open('data/'+name+'_'+"pulls_2019-10-30_2020-04-30" + '.csv', 'a', newline='',encoding="utf-8") as csvfile:
                f1w = csv.writer(csvfile)
                f1w.writerow(dat)

        for num in range(num_pages_pulls):
            link = "/pulls?page="+str(num+1)+"&q=is%3Apr+is%3Aclosed+closed%3A2019-10-30..2020-04-30"
            link = base_url + link
            returns = load_base(link)
            time.sleep(5)
            objects = outer_page(returns[0], returns[1])
            with open('data/'+name+'_'+"pulls_2019-10-30_2020-04-30" + '.csv', 'a', newline='',encoding="utf-8") as csvfile:
                f1w = csv.writer(csvfile)
                for _obj in objects:
                    f1w.writerow(_obj)


# In[172]:
main()

