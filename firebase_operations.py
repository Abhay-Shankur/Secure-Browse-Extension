import time
import firebase_admin
from firebase_admin import credentials, db


class FirebaseOperations:
    def __init__(self):
        # Initialize Firebase with your service account key
        self.cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self.cred,
                                      {'databaseURL': 'https://detect-f07fd-default-rtdb.firebaseio.com'})


class RealtimeDatabaseListener(FirebaseOperations):
    def __init__(self):
        super().__init__()
        self.updated_value = None

    def callback(self, event):
        if event.event_type == 'put' and event.data != -1:
            # Value updated
            # updated_value = /
            self.updated_value = event.data
            # print(f"Value at location {event.path} updated to: {self.updated_value}")
            return

    def start_listener(self, location):
        ref = db.reference(location)
        self.updated_value = ref.get()
        ref.listen(self.callback)
        while True:
            if self.updated_value != -1:
                return self.updated_value
        return None

    def remove_location(self, location):
        ref = db.reference(location)
        ref.delete()
        print(f"Location {location} removed.")

    def add_value(self, path, data):
        db.reference(path).update(data)



# Example usage
# fbrd = RealtimeDatabaseListener()
# if fbrd.start_listener('/Tokens/hAoa1FBmFu') != -1:
#     fbrd.remove_location('/Tokens/hAoa1FBmFu')
