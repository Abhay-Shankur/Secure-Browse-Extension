import time
import firebase_admin
from firebase_admin import credentials
from firebaseoperations.firestore_database import FirebaseDataConnect
# from firebaseoperations.realtime_database import RealtimeDatabaseListener


class FirebaseOperations(FirebaseDataConnect):
    def __init__(self):
        # FirebaseDataConnect()
        # RealtimeDatabaseListener()
        # Initialize Firebase with your service account key
        self.cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self.cred,)
        super().__init__()
