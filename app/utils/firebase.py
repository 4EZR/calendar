import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin import firestore

cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

def validate_token(id_token):
    try:

        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except auth.InvalidIdTokenError:
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# def disable_account(user_id):
#     
