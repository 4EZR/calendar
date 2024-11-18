import os
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin import firestore

from dotenv import load_dotenv
load_dotenv()

credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

cred = credentials.Certificate(credentials)
firebase_admin.initialize_app(cred)


db = firestore.client()

def validate_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return {
            'valid': True,
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'name': decoded_token.get('name')
        }
    except auth.InvalidIdTokenError:
        return {'valid': False, 'error': 'Invalid token'}
    except auth.ExpiredIdTokenError:
        return {'valid': False, 'error': 'Token expired'}
    except Exception as e:
        return {'valid': False, 'error': str(e)}

# def disable_account(user_id):
#     
