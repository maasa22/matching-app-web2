# pipenv shell
# pipenv install firebase-admin
# https://qiita.com/yusukeito58/items/c77feaa25fbbe37e9953

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid

# Use a service account
cred = credentials.Certificate('./matching-app-web2-firebase-adminsdk-y9zo7-579383bf26.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Craete data
def createData():
    doc_ref = db.collection('todos').document(str(uuid.uuid4()))
    doc_ref.set({
        'limit': 'tommorow',
        'todo': 'go to a cafe',
    })

# Read data
def readData():
    users_ref = db.collection(u'todos')
    docs = users_ref.stream()
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

# Update data

# Delete data
