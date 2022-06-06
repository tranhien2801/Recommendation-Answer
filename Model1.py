import pandas as pd
import pymongo
import numpy as np
import string
import pickle
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from vncorenlp import VnCoreNLP
from ocr import ocr_text

import json




# Chuyển về path lưu VnCoreNLP-1.1.1.jar
annotator = VnCoreNLP("D:\ElcomAI\VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg,pos", max_heap_size='-Xmx2g')

def get_stopwords_list(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))

stopwords_path = 'input/vietnamese-stopwords'
stopwords_list = get_stopwords_list(stopwords_path)

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['colearn_textbook1']
colCategories = mydb["categories"]
colAnswers = mydb["answers"]


cursor = colCategories.find({'has_sub_category': 0})
all_data = pd.DataFrame(list(cursor))
all_data.dropna(axis=0)
all_data.drop_duplicates(subset='name')
name = all_data['name']
all_data['name'] = all_data['name'].str.replace('\n', ' ')

lemmatizer = WordNetLemmatizer()


def my_tokenizer(doc):
    tok = annotator.tokenize(doc)
    non_stopwords = [w for w in tok[0] if not w[0] in stopwords_list]
    non_punctuation = [w for w in non_stopwords if not w[0] in string.punctuation]
    print(non_punctuation)
    return non_punctuation



# tfidf_vectorizer = TfidfVectorizer(tokenizer=my_tokenizer)
# tfidf_matrix = tfidf_vectorizer.fit_transform(tuple(all_data['name']))
# pickle.dump(tfidf_vectorizer, open("crawlData/myvectorizer.pickle", "wb"))
# sparse.save_npz("crawlData/mymatrix.npz", tfidf_matrix)

tfidf_vectorizer = pickle.load(open("crawlData/myvectorizer.pickle", "rb"))
tfidf_matrix = sparse.load_npz("crawlData/mymatrix.npz")

def ask_question(question):
    query_vect = tfidf_vectorizer.transform([question])
    similarity = cosine_similarity(query_vect, tfidf_matrix)
    max_similarity = np.argmax(similarity, axis=None)

    if (np.amax(similarity, axis=None) > 0.3):
        print('Closest question found:', name.iloc[max_similarity])
        print('Similarity: {:.2%}'.format(similarity[0, max_similarity]))
        answer = pd.DataFrame(list(colAnswers.find({'category_id': all_data.iloc[max_similarity]['_id']})))
        print('Answer: ', answer['content'][0])
    else :
        print("Sorry, I didn't get you.")
       
       
data = {
    "question_content": "Câu: Dựa vào phong trào kháng chiến của nhân dân, phái chủ chiến trong triều đình Huế, đại diện là những ai mạnh tay hành động chống Pháp?",
    "question_img": 'https://static.colearn.vn:8413/v1.0/upload/qa/image/17042022/colearn-E6NfWx.jpg'
}       
        
        
def main():
    question = data['question_content']
    ask_question(question)
    questions = ocr_text.convertImgtoText(data['question_img'])
    for question in questions:
        ask_question(question)

        

if __name__ == '__main__':
    main()   
        
        
        

# question_active = True

# while question_active:
#     question_user = input('Type your question here: ')
#     url = 'https://static.colearn.vn:8413/v1.0/upload/store/image/18042022/df131b08-153a-4fbc-8c75-1235da446454.jpeg'
#     question_user = ocr_text.convertImgtoText(url)
#     print(question_user)
#     for question in question_user:
#         ask_question(question)
#     response = input('Do you have any questions? (y/n)')
#     if response == 'n':
#         question_active = False
#         print("Good bye!")


