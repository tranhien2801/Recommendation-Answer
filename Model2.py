import pandas as pd
import pymongo
import numpy as np
import string
import pickle
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from vncorenlp import VnCoreNLP

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
print(len(all_data))
all_data.dropna(axis=0)
all_data.drop_duplicates(subset='name')
name = all_data['name']
all_data['name'] = all_data['name'].str.replace('\n', ' ')
print(all_data['name'][0])

lemmatizer = WordNetLemmatizer()


def my_tokenizer(doc):
    pos_tags = annotator.pos_tag(doc)
    non_stopwords = [w for w in pos_tags[0] if not w[0] in stopwords_list]
    non_punctuation = [w for w in non_stopwords if not w[0] in string.punctuation]
    lemmas = []
    # cần xem lại mấy cái pos_tag của vncorenlp là gì để sửa mô hình
    for w in non_punctuation:
        if w[1].startswith('J'):
            pos = wordnet.ADJ
        elif w[1].startswith('V'):
            pos = wordnet.VERB
        elif w[1].startswith('N'):
            pos = wordnet.NOUN
        elif w[1].startswith('R'):
            pos = wordnet.ADV
        else:
            pos = wordnet.NOUN
        lemmas.append(lemmatizer.lemmatize(w[0], pos))
    print(lemmas)
    return lemmas



tfidf_vectorizer = TfidfVectorizer(tokenizer=my_tokenizer)
tfidf_matrix = tfidf_vectorizer.fit_transform(tuple(all_data['name']))
pickle.dump(tfidf_vectorizer, open("crawlData/vectorizer2.pickle", "wb"))
sparse.save_npz("crawlData/matrix2.npz", tfidf_matrix)

# tfidf_vectorizer = pickle.load(open("crawlData/vectorizer2.pickle", "rb"))
# tfidf_matrix = sparse.load_npz("crawlData/matrix2.npz")

def ask_question(question):
    query_vect = tfidf_vectorizer.transform([question])
    similarity = cosine_similarity(query_vect, tfidf_matrix)
    max_similarity = np.argmax(similarity, axis=None)

    if (np.amax(similarity, axis=None) > 0.0):
        print('Closest question found:', name.iloc[max_similarity])
        print('Similarity: {:.2%}'.format(similarity[0, max_similarity]))
        answer = pd.DataFrame(list(colAnswers.find({'category_id': all_data.iloc[max_similarity]['_id']})))
        print('Answer: ', answer['content'][0])
    else :
        print("Sorry, I didn't get you.")

question_active = True

while question_active:
    question_user = input('Type your question here: ')
    ask_question(question_user)
    response = input('Do you have any questions? (y/n)')
    if response == 'n':
        question_active = False
        print("Good bye!")


