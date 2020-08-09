# pipenv shell
# pipenv install firebase-admin
# https://qiita.com/yusukeito58/items/c77feaa25fbbe37e9953

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
import datetime
import random

# Use a service account
cred = credentials.Certificate('./matching-app-web2-firebase-adminsdk-y9zo7-579383bf26.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Craete data
def createData():
    doc_ref = db.collection('users').document(str(uuid.uuid4().hex))
    doc_ref.set({
        'display_name': 'ナオキ',
        'age': 25,
        'gender': 'male', \
        'mail' : 'hoge@hoge',\
        'birthday' : datetime.datetime(1994, 2, 8, 1, 40, 27, 425337) ,\
        'prefecture' : '東京都', \
        'status_message' : 'よろしくお願いします',\
        'profile_images' : 'images/man1.jpg',\
        'introduction' : 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s...',\
        'got_favorites' : 48,\
        'last_login' : '24時間以内'
        # datetime.date(1994, 11, 18)
        # datetime.datetime(2010, 2, 8, 1, 40, 27, 425337)\
    })

# Read data
def readData():
    users_ref = db.collection('users')
    docs = users_ref.stream()
    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))

# Update data

# Delete data
def deleteData():
    users_ref = db.collection(u'users')
    docs = users_ref.limit(100).get()
    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()


# readData()
deleteData()
# createData()

display_name_list = ['マナツ', 'エリカ', 'ミナミ', 'アスカ', 'ミヅキ']
age_list = [25,26,27,28,29]
mail_list = ["a@a", "b@b", "c@c", "d@d", "e@e"]
prefecture_list = ['東京都', '埼玉県', '神奈川県']
status_message_list = ['よろしくお願いします！', 'こんにちは', 'Lorem Ipsum is simply dummy text']
profile_images_list = ['images/woman1.jpg', 'images/woman2.jpg', 'images/woman3.jpg']
for i in range(5):
    doc_ref = db.collection('users').document(str(uuid.uuid4().hex))
    doc_ref.set({
        'display_name': random.choice(display_name_list),
        'gender': 'female', \
        # 'email' : mail_list[i],\
        'prefecture' : random.choice(prefecture_list), \
        'status_message' : random.choice(status_message_list),\
        'profile_images' : random.choice(profile_images_list),\
        'introduction' : 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s...',\
        'birthday' : datetime.datetime(1994, 2, 8, 1, 40, 27, 425337) ,\
        'age': random.choice(age_list),
        'got_favorites' : 48,\
        'last_login_batch' : '24時間以内', \
        'last_login' : datetime.datetime.now()
        # datetime.date(1994, 11, 18)
        # datetime.datetime(2010, 2, 8, 1, 40, 27, 425337)\
    })

display_name_list = ['ナオキ', 'ハヤト', 'ヨシヒロ', 'カズマ', 'ヒロユキ']
mail_list = ["f@f", "g@g", "h@h", "i@i", "j@j"]
profile_images_list = ['images/man1.jpg', 'images/man2.jpg', 'images/man3.jpg']

for i in range(5):
    doc_ref = db.collection('users').document(str(uuid.uuid4().hex))
    doc_ref.set({
        'display_name': random.choice(display_name_list),
        'gender': 'male', \
        # 'email' : mail_list[i],\
        'prefecture' : random.choice(prefecture_list), \
        'status_message' : random.choice(status_message_list),\
        'profile_images' : random.choice(profile_images_list),\
        'introduction' : 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s...',\
        'birthday' : datetime.datetime(1994, 2, 8, 1, 40, 27, 425337) ,\
        'age': random.choice(age_list),
        'got_favorites' : 48,\
        'last_login_batch' : '24時間以内', \
        'last_login' : datetime.datetime.now()
        # datetime.date(1994, 11, 18)
        # datetime.datetime(2010, 2, 8, 1, 40, 27, 425337)\
    })

# # batch udpates: age, favorites, last_login
# # realtime updates: display_name, self_images, self_introduction, prefecture
