import requests
import pymongo
import re
from bs4 import BeautifulSoup

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['colearn_textbook1']
colAnswers = mydb["answers"]
colCategories = mydb["categories"]

urlBase = "https://vietjack.com/"

def crawlInEx(url, parent):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    soup.prettify(formatter="html5")
    checkExist1 = soup.find('b', string="Lời giải:")
    checkExist2 = soup.find('b', string="Trả lời:")
    checkExist = checkExist1 or checkExist2
    if checkExist != None:
        question = soup.find(attrs={"style": "color:green;"}).parent
        name = question.text
        temp = question.next_sibling
        while temp.next_element.text != 'Lời giải:' and temp.next_element.text != "Trả lời:":
            if temp.name == 'p':
                name += '\n' + temp.text
                if temp.find('img'):
                    name += '\n' + urlBase + temp.find('img').get('src')[2:]
            if temp.name == 'img':
                name += '\n' + urlBase + temp.get('src')[2:]
            if temp.name == 'table':
                name += '\n' + temp.prettify()
            temp = temp.next_sibling
        print(name)
        print('------------')
        temp = temp.next_sibling.next_sibling
        content = ''

        while temp.next_sibling.name != 'ul':
            if temp.name == 'p' and temp.find(string=lambda text: "giải bài tập" in text.lower()) == None:
                content += temp.text + '\n'
                if temp.find('img'):
                    content += urlBase + temp.find('img').get('src')[2:] + '\n'
            if temp.name == 'img':
                content += urlBase + temp.get('src')[2:] + '\n'
            if temp.name == 'table':
                content += temp.prettify() + '\n'
            temp = temp.next_sibling
        print(content)
        colCategories.insert_one({'parent_id': parent['_id'], 'name': name, 'has_sub_category': 0})
        category_id = colCategories.find_one({'name': name})
        colAnswers.insert_one({'category_id': category_id['_id'], 'content': content})

def crawlInUnit(url, parent):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    execises = soup.find('ul', class_='list').find_all('li')
    for execise in execises:
        try:
            crawlInEx(urlBase + execise.find('a').get('href')[2:], parent)
        except: print("error")


def crawlInSubject(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    chapters = soup.findAll('b', attrs={"style": "color:blue;"}, string=lambda text: "chương" in text.lower())
    if chapters == None:
        chapters = soup.findAll('b', attrs={"style": "color:blue;"}, string=lambda text: "unit" in text.lower())
    subject = soup.find('h1', class_='title')
    print(subject.text)
    colCategories.insert_one({'name': subject.text, 'has_sub_category': 1})
    subject = colCategories.find_one({'name': subject.text})
    for chapter in chapters:
        chapter = chapter.parent.parent
        print("-------------------------")
        print(chapter.text)
        colCategories.insert_one({'parent_id': subject['_id'] ,'name': chapter.text, 'has_sub_category': 1})
        units = chapter.next_sibling.next_sibling.find_all('li')
        chapter = colCategories.find_one({'name': chapter.text})
        for unit in units:
            print(unit.text)
            colCategories.insert_one({'parent_id': chapter['_id'], 'name': unit.text, 'has_sub_category': 1})
            parent = colCategories.find_one({'name': unit.text})
            crawlInUnit(urlBase + unit.find('a').get('href')[2:], parent)

def crawlInClass (url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    links = soup.findAll('b', string=lambda text: "giải bài tập" in text.lower())
    for link in links:
        if "toán" not in link.text.lower() and "vật lý" not in link.text.lower() \
                and "hóa học" not in link.text.lower() and "vật lí" not in link.text.lower():
            try:
                crawlInSubject(urlBase + link.parent.get('href')[2:])
            except: print("Lỗi rồi")

def crawlInHome(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    links = soup.findAll('li', class_='level-1')
    for i in range(6, len(links) - 1):
        crawlInClass(urlBase + links[i].find('a').get('href')[2:])


crawlInHome("https://vietjack.com//index.jsp")

