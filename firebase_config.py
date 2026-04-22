import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Initialize Firebase
cred_json = os.getenv('FIREBASE_CREDENTIALS')

if cred_json:
    # Production: use env variable
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
else:
    # Development: use local file (if exists)
    try:
        cred = credentials.Certificate('firebase-key.json')
    except:
        cred = None

if cred:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://gen-lang-client-0661551951-default-rtdb.asia-southeast1.firebaseio.com'
    })

def get_db():
    """Get Firebase Realtime Database reference"""
    return db.reference()
