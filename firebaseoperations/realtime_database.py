import threading
from firebase_admin import db


class RealtimeDatabaseListener:
    def __init__(self):
        self.updated_value = None
        self.listener = None  # Added a listener attribute

    def callback(self, event):
        if event.event_type == 'put':
            self.updated_value = event.data
            return

    def start_listener(self, location):
        ref = db.reference(location)
        self.updated_value = dict(ref.get())

        # Close the previous listener if exists
        if self.listener:
            self.listener.close()

        # Start a new listener
        self.listener = ref.listen(self.callback)

        # Wait for an update with a child named "result"
        while True:
            if "verified" in self.updated_value.keys():
                return self.updated_value

    def remove_location(self, location):
        ref = db.reference(location)
        ref.delete()
        print(f"Location {location} removed.")

    def add_value(self, path, data):
        db.reference(path).update(data)
