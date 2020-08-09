# pipenv shell
# pipenv install firebase-admin
# https://qiita.com/yusukeito58/items/c77feaa25fbbe37e9953

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
from datetime import datetime
import config
import random

# Use a service account
cred = credentials.Certificate('./matching-app-web2-firebase-adminsdk-y9zo7-579383bf26.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Craete data
def createData():
    doc_ref = db.collection('messages').document(str(uuid.uuid4().hex))
    doc_ref.set({
        'message': 'How are you?', \
        'sender' : 'hoge@hoge',\
        'receiver' : 'hoge2@hoge'
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
    users_ref = db.collection(u'messages')
    docs = users_ref.limit(100).get()
    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()


# readData()
deleteData()
# createData()
doc_ref = db.collection('messages').document(str(uuid.uuid4().hex))
doc_ref.set({
    'message': 'How are you?', \
    'sender' : config.MAIL1,\
    'receiver' : config.MAIL2,\
    'createdAt' : datetime.now()
})

doc_ref = db.collection('messages').document(str(uuid.uuid4().hex))
doc_ref.set({
    'message': 'I\'m super fine?', \
    'sender' : config.MAIL2,\
    'receiver' : config.MAIL1, \
    'createdAt' : datetime.now()
})
