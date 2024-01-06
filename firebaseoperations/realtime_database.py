from firebase_admin import db


class RealtimeDatabaseListener():
    def __init__(self):
        # super().__init__()
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
        return

    def remove_location(self, location):
        ref = db.reference(location)
        ref.delete()
        print(f"Location {location} removed.")

    def add_value(self, path, data):
        db.reference(path).update(data)

