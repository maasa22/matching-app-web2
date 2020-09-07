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
status_message_list = ['よろしくお願いします！', 'こんにちは', 'Hi, there! What\'s up']
#profile_images_list = ['/images/woman1.jpg', '/images/woman2.jpg', '/images/woman3.jpg', '/images/woman4.jpg', '/images/woman5.jpg', '/images/woman6.jpg']
profile_images_list = [
    "https://firebasestorage.googleapis.com/v0/b/matching-app-web2.appspot.com/o/imgs%2Fwoman1.jpg?alt=media&token=11c94484-d2da-48ee-92a7-4483696edfc1",\
    "https://firebasestorage.googleapis.com/v0/b/matching-app-web2.appspot.com/o/imgs%2Fwoman2.jpg?alt=media&token=14cc784e-6f42-476e-a3fd-464a957c8b70", \
    "https://firebasestorage.googleapis.com/v0/b/matching-app-web2.appspot.com/o/imgs%2Fwoman3.jpg?alt=media&token=5f1f0c0c-dfc7-46d2-8672-ec6bb3c61557", \
]
introductions_list = [
    "こんにちは。プロフィール見て下さりありがとうございます^^ 練馬区の病院で看護師しています♪ 女性ばかりの職場で中々いい出会いがなく、思い切って登録してみることにしました！",
    "美味しい物が大好きで、趣味はカフェ巡りや、お店探しです。最近は料理にも挑戦中です😎 特にカフェごはんが好きで、恵比寿や代官山によく行きます。恵比寿や代官山は安くて美味しい隠れ家的なカフェが多いので好きです♩ ロコモコを食べて、紅茶とケーキを頂き友達と喋りながらゆっくり過ごすのが至福のときです☺",
]
for i in range(3):
    doc_ref = db.collection('users').document(str(uuid.uuid4().hex))
    doc_ref.set({
        'display_name': random.choice(display_name_list),
        'gender': 'female', \
        # 'email' : mail_list[i],\
        'prefecture' : random.choice(prefecture_list), \
        'status_message' : random.choice(status_message_list),\
        'profile_images' : random.choice(profile_images_list),\
        'introduction' : random.choice(introductions_list),\
        'birthday' : datetime.datetime(1994, 2, 8, 1, 40, 27, 425337) ,\
        'age': random.choice(age_list),
        # 'acquired_favorites' : 48,\
        # 'available_favorites' : 30,\
        # 'last_login_batch' : '24時間以内', \
        # 'last_login' : datetime.datetime.now()
        # datetime.date(1994, 11, 18)
        # datetime.datetime(2010, 2, 8, 1, 40, 27, 425337)\
    })

display_name_list = ['ナオキ', 'ハヤト', 'ヨシヒロ', 'カズマ', 'ヒロユキ']
mail_list = ["f@f", "g@g", "h@h", "i@i", "j@j"]
#profile_images_list = ['images/man1.jpg', 'images/man2.jpg', 'images/man3.jpg']
profile_images_list = [
    "https://firebasestorage.googleapis.com/v0/b/matching-app-web2.appspot.com/o/imgs%2Fman1.jpg?alt=media&token=15b1644e-9ec1-47da-9b09-5bac6780c147", \
    "https://firebasestorage.googleapis.com/v0/b/matching-app-web2.appspot.com/o/imgs%2Fman2.jpg?alt=media&token=40aa514f-4bdb-4517-b04f-5b7aa7ae8b86", \
    "https://firebasestorage.googleapis.com/v0/b/matching-app-web2.appspot.com/o/imgs%2Fman3.jpg?alt=media&token=3d7c3c1c-b8c6-426d-9680-b284915c6822", \
    ]
introductions_list = [
    "初めまして。プロフィールを見ていただきありがとうございます！ 東京で営業の仕事をしていますが、日々忙しくなかなか出会いがなかったので登録しました。",
    "趣味はスポーツ、アウトドア、ドライブです。 昔ラグビーをしていたので、体格はがっちりしています。職場ではよく「プーさん」に似ていると言われています(笑) ラグビー以外にもスポーツ全般の観戦が大好きで、友人と野球観戦によく行きます。ちなみに広島カープファンです！",
]

for i in range(3):
    doc_ref = db.collection('users').document(str(uuid.uuid4().hex))
    doc_ref.set({
        'display_name': random.choice(display_name_list),
        'gender': 'male', \
        # 'email' : mail_list[i],\
        'prefecture' : random.choice(prefecture_list), \
        'status_message' : random.choice(status_message_list),\
        'profile_images' : random.choice(profile_images_list),\
        'introduction' : random.choice(introductions_list),\
        'birthday' : datetime.datetime(1994, 2, 8, 1, 40, 27, 425337) ,\
        'age': random.choice(age_list),
        #'acquired_favorites' : 46,\
        #'available_favorites' : 20,\
        #'last_login_batch' : '24時間以内', \
        #'last_login' : datetime.datetime.now()
        # datetime.date(1994, 11, 18)
        # datetime.datetime(2010, 2, 8, 1, 40, 27, 425337)\
    })

# # batch udpates: age, favorites, last_login
# # realtime updates: display_name, self_images, self_introduction, prefecture
