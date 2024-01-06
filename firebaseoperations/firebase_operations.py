import time
import firebase_admin
from firebase_admin import credentials
from firebaseoperations.firestore_database import FirebaseDataConnect
from firebaseoperations.realtime_database import RealtimeDatabaseListener


class FirebaseOperations(FirebaseDataConnect, RealtimeDatabaseListener):
    def __init__(self):
        # FirebaseDataConnect()
        # RealtimeDatabaseListener()
        # Initialize Firebase with your service account key
        self.cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self.cred,
                                      {'databaseURL': 'https://detect-f07fd-default-rtdb.firebaseio.com'})
        super().__init__()

    # def get_firestore_instance(self):
    #     return firestore_database()
    #
    # def get_database_instance(self):
    #     return realtime_database();


# Example usage
# fbrd = RealtimeDatabaseListener()
# if fbrd.start_listener('/Tokens/hAoa1FBmFu') != -1:
#     fbrd.remove_location('/Tokens/hAoa1FBmFu')
