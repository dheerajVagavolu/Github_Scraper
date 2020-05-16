import requests
from bs4 import BeautifulSoup
import time
#class = social_count
def get_social_count(soup_obj):
    counts = soup_obj.find_all('a', class_='social-count')
    for count in counts:
        if 'stargazers' in count['href']:
            f.write('Stars: '+removek(count.text.strip()) +'\n')
        if 'members' in count['href']:
            f.write('Forks: '+removek(count.text.strip()) + '\n')

#class  = topic-tag
def get_tags(soup_obj):
    f.write('Tags:')
    tags = soup_obj.find_all('a', 'topic-tag')
    for i in tags:
        f.write(' '+i.text.strip())
    f.write('\n\n')

#Convert string representation to integer! 8.2k -> 8200
def removek(num):
    if num.find('k')!=-1:
        new_num = num[:-1]
        return str(int(float(new_num)*1000))
    else:
        return str(num)

def get_summary(soup_obj):
    
    summary = soup_obj.find('ul', 'numbers-summary')
    objects = summary.find_all('li')

    for obj in objects:
        name = obj.find('a')['href']
        
        if 'releases' in name:
            f.write("Releases: "+preprocess(obj.text)+'\n')
        if 'contributors' in name:
            f.write("Contributors: "+preprocess(obj.text)+'\n')

def preprocess(text):
    text = text.strip().split(' ')[0]
    text = text.replace(' ','')
    text = text.replace('\n','')
    text = text.replace('\t','')
    return text

def check(soup_obj):
    summary = soup_obj.find('ul', 'numbers-summary')
    objects = summary.find_all('li')

    test = 0
    for obj in objects:
        name = obj.find('a')['href']
        
        
        if 'contributors' in name:
            try:
                t = int(preprocess(obj.text))
                test = 1
            except:
                test = 0
                
    
    return test

def create_log(URL):
    global f
    f = open('../data/data','a')
    
    print("Getting the page ..... ")
    
    page = requests.get(URL.strip())
    time.sleep(2)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Comment to remove force load. The contributions will not properly load because it is fetched a little late using JS.
    if check(soup) == 0:
        return 0

    f.write(get_name(URL)+'\n'+'-'*len(get_name(URL))+'\n')
    get_summary(soup)
    get_social_count(soup)
    get_tags(soup)
    f.close()
    return 1

def get_name(repo):
    return repo.replace('https://github.com/', '').strip()


    
        
    