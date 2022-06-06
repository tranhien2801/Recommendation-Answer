import requests
import pymongo
import re
from bs4 import BeautifulSoup

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['mydatabase']
mycol = mydb["database"]

def crawNewsData(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    titles = soup.findAll(string=lambda text: "Câu" in text)
    for title in titles:
        tag = title.parent.parent
        # print(tag.parent.name)
        if tag.name == "p" and tag.parent['class'] != 'show-answer':
            question = title.parent.parent.text
            print(question)
            temp = title.parent.parent.next_sibling
            # print(temp.next_sibling.text)
            answerA = answerB = answerC = answerD = ''

            while temp.name != 'section':
                if temp.text.strip()[:1] == 'A' or temp.text.strip()[:1] == 'a':
                    answerA = temp.text.replace("\n", "")
                    print(answerA)
                if temp.text.strip()[:1] == 'B' or temp.text.strip()[:1] == 'b':
                    answerB = temp.text.replace("\n", "")
                    print(answerB)
                if temp.text.strip()[:1] == 'C' or temp.text.strip()[:1] == 'c':
                    answerC = temp.text.replace("\n", "")
                    print(answerC)
                if temp.text.strip()[:1] == 'D' or temp.text.strip()[:1] == 'd':
                    answerD = temp.text.replace("\n", "")
                    print(answerD)
                temp = temp.next_sibling

            answer = temp.text
            print(answer)
            # mycol.insert_one({'Question': question, 'Answer': answer, 'AnswerA': answerA,
            #                   'AnswerB': answerB, 'AnswerC': answerC, 'AnswerD': answerD})

def crawlLink(urlBase, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.findAll('a', class_='cate')
    for link in links:
        print(urlBase + link.get('href'))
        try :
            crawNewsData(urlBase + link.get('href'))
        except:
            print("Lỗi gì đấy!!!")




# crawlLink("https://sachgiaokhoa.info","https://sachgiaokhoa.info/lop-7/ly-thuyet-600-cau-trac-nghiem-dia-li-7")

# crawNewsData("https://sachgiaokhoa.info/lop-7/ly-thuyet-500-cau-trac-nghiem-cong-nghe-7-co-dap-an/ly-thuyet-trac-nghiem-bai-30-vai-tro-va-nhiem-vu-phat-trien-chan-nuoi-cong-nghe-7-wbi")


def crawlInClass(urlBase, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.findAll('a', href=re.compile("trac-nghiem"))
    # print(links)
    for link in links:
        # print(urlBase + link.get('href'))
        crawlLink(urlBase, urlBase + link.get('href'))

crawlInClass("https://sachgiaokhoa.info","https://sachgiaokhoa.info/lop-12")