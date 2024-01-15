import time
import firebase_admin
from firebase_admin import credentials
from firebaseoperations.firestore_database import FirebaseDataConnect


class FirebaseOperations(FirebaseDataConnect):
    def __init__(self, app_name):
        # Initialize Firebase with your service account key
        self.cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self.cred, {'appName': app_name})
        super().__init__()
