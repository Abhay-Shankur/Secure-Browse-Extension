import threading

from firebase_admin import firestore


class FirebaseDataConnect:

    def __init__(self):
        self.db = None
        self.listener = None

    def initialize_firestore(self):
        self.db = firestore.client()

    def close_firestore(self):
        if self.db:
            self.db.close()

    # Function to fetch data from Firebase
    # def fetch_data_from_firebase(self):
    #     # Assuming you have a collection named 'data' and a document with field 'datastring'
    #     # doc_ref = self.db.collection('users').document('your_document_id')
    #     doc_ref = self.db.collection('users')
    #     print(doc_ref)
    #     # data = doc_ref.get().to_dict().get('datastring', '')
    #     # return data

    def get_all_collections(self):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        # Retrieve all collections by listing all documents in the root
        collections = [collection.id for collection in self.db.collections()]

        # Close Firestore connection after the operation
        self.close_firestore()

        return collections

    # Function to Add Documents
    def add_doc(self, collection_name="Credentials", doc=None, doc_id=None):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        val = self.db.collection(collection_name).document(doc_id).set(doc)

        # Close Firestore connection after the operation
        self.close_firestore()

        return val

    def get_all_document_fields(self, collection_name="Credentials", document_id=None):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        document_ref = self.db.collection(collection_name).document(document_id)
        document_data = document_ref.get().to_dict()

        # Close Firestore connection after the operation
        self.close_firestore()

        return document_data

    def get_all_documents(self, collection_name="Credentials"):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        collection_ref = self.db.collection(collection_name)
        documents = collection_ref.stream()

        # Close Firestore connection after the operation
        self.close_firestore()
        return documents

    def display_document_names(self, collection_name="Credentials"):
        all_documents = self.get_all_documents(collection_name=collection_name)
        return [document.id for document in all_documents]
        # for document in all_documents:
        #     print(f"Document ID: {document.id}")

    def get_matching_doc(self, collection_name="Credentials"):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        ref = self.db.collection(collection_name)
        total_doc = ref.get()

        total_count = len(total_doc)
        active_count = sum(1 for doc in total_doc if doc.to_dict().get('age') == 40)
        on_leave_count = sum(1 for doc in total_doc if doc.to_dict().get('age') == 30)

        data = {
            "collection": collection_name,
            "total": total_count,
            "total-active": active_count,
            "total-onleave": on_leave_count
        }

        # Close Firestore connection after the operation
        self.close_firestore()

        return data
        # print(total_count, active_count, on_leave_count)

    def get_updated_document(self, collection_name="Credentials", document_id=None):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        document_ref = self.db.collection(collection_name).document(document_id)

        # Use threading.Event to signal when the document is updated
        update_event = threading.Event()

        def callback(snapshot, changes, read_time):
            # Check if the document has been updated
            if changes:
                for change in changes:
                    if change.type.name == 'MODIFIED':
                        update_event.set()

        # Start listening for changes to the document
        self.listener = document_ref.on_snapshot(callback)

        # Wait for the document to be updated
        update_event.wait()

        # Get the updated document
        updated_document = document_ref.get().to_dict()

        # Stop the listener to avoid resource leaks
        if self.listener:
            self.listener.unsubscribe()

        # Close Firestore connection after the operation
        self.close_firestore()

        return updated_document

    def close_connection(self):
        # Stop the listener before closing the connection
        if self.listener:
            self.listener.unsubscribe()

        # Close Firestore connection if not already closed
        self.close_firestore()