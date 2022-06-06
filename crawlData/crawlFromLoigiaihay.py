import requests
import pymongo
import re
from bs4 import BeautifulSoup

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['mydatabase']
mycol = mydb["database"]


def crawNewsData(url):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    titles = soup.findAll('div', class_='question')
    for title in titles:
        question = title.findAll('p')[1].text
        print(question)
        answerA = answerB = answerC = answerD = ''
        ans = title.findAll('li')
        if len(ans) > 0:
            answerA = ans[0].text
            print(answerA)
        if len(ans) > 1:
            answerB = ans[1].text
            print(answerB)
        if len(ans) > 2:
            answerC = ans[2].text
            print(answerC)
        if len(ans) > 3:
            answerD = ans[3].text
            print(answerD)
        answer = title.find('div', class_='loigiai').find('p').text
        print(answer)
        # mycol.insert_one({'Question': question, 'Answer': answer, 'AnswerA': answerA,
        #                 'AnswerB': answerB, 'AnswerC': answerC, 'AnswerD': answerD})

def crawlLink(urlBase, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.findAll('a', class_='n-exercise')
    for link in links:
        crawNewsData(urlBase + link.get('href'))

def crawlSubject(urlBase, url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    uls = soup.findAll('ul', class_='list-posts')
    for ul in uls:
        links = ul.findAll('li', class_='clearfix')
        for link in links:
            # try:
                if link.find('a').get('href')[:5] == "https":
                    crawlLink(urlBase, link.find('a').get('href'))
                else:
                    crawlLink(urlBase, urlBase + link.find('a').get('href'))
            # except:
            #     print("Lỗi gì đấy!!!")


def crawlClass(urlBase, url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find('div', class_='n-form-sub')
    links = content.findAll('a', href=re.compile("trac-nghiem"))
    for link in links:
        crawlSubject(urlBase, urlBase + link.get('href'))

def crawlHome(urlBase):

    response = requests.get(urlBase)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.findAll('li', class_='menu-haschild')
    for link in links:
        crawlClass(urlBase, urlBase + link.find('a').get('href'))

crawlHome("https://loigiaihay.com")
# crawlSubject("https://loigiaihay.com", "https://loigiaihay.com/trac-nghiem-hoa-10-c583.html")
# crawlClass("https://loigiaihay.com", "https://loigiaihay.com/lop-10.html")
