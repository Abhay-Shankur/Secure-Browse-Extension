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

    def close_connection(self):
        # Stop the listener before closing the connection
        if self.listener:
            self.listener.unsubscribe()

        # Close Firestore connection if not already closed
        self.close_firestore()

    # Function to Add Documents
    def add_doc(self, collection_name="Credentials", doc=None, doc_id=None):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        val = self.db.collection(collection_name).document(doc_id).set(doc)

        # Close Firestore connection after the operation
        self.close_firestore()

        return val

    # Function to get all Collection
    def get_all_collections(self):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        # Retrieve all collections by listing all documents in the root
        collections = [collection.id for collection in self.db.collections()]

        # Close Firestore connection after the operation
        self.close_firestore()

        return collections

    # Function to get all documents from Collection
    def get_all_documents(self, collection_name="Credentials"):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        collection_ref = self.db.collection(collection_name)
        documents = collection_ref.stream()

        # Close Firestore connection after the operation
        self.close_firestore()
        return documents

    # Function to get document data from a collection
    def get_all_document_fields(self, collection_name="Credentials", document_id=None):
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        document_ref = self.db.collection(collection_name).document(document_id)
        document_data = document_ref.get().to_dict()

        # Close Firestore connection after the operation
        self.close_firestore()

        return document_data

    # To get All Documents ID of a Collection
    def display_document_names(self, collection_name="Credentials"):
        all_documents = self.get_all_documents(collection_name=collection_name)
        return [document.id for document in all_documents]

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

    # Function to get updated Document
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

    # Function to add values to a list
    def set_value_to_list_field(self, collection_name="ORG", document_id=None, field_name=None, new_value=None):
        """
        Add a value to a list field in a specific document.

        Args:
        - collection_name (str): The name of the collection.
        - document_id (str): The ID of the document to update.
        - field_name (str): The name of the list field.
        - new_value: The value to add to the list.

        Returns:
        - bool: True if the update is successful, False otherwise.
        """
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        try:
            # Get the reference to the document
            document_ref = self.db.collection(collection_name).document(document_id)
            # Get the current state of the document
            doc_snapshot = document_ref.get()
            doc_data = doc_snapshot.to_dict()

            # Update the set field based on the type of new_value
            if isinstance(new_value, dict):
                # If new_value is a dictionary, update with its key-value pair
                current_set = dict(doc_data.get(field_name, []))
                for key, value in new_value.items():
                    current_set[key] = value
                document_ref.update({field_name: current_set})
            else:
                # If new_value is a single value, update the set field
                current_set = set(doc_data.get(field_name, []))
                current_set.add(new_value)
                document_ref.update({field_name: list(current_set)})

            # Close Firestore connection after the operation
            self.close_firestore()

            return True
        except Exception as e:
            print(f"Error updating document: {e}")

            # Close Firestore connection after the operation
            self.close_firestore()

            return False

    def get_list_field_values(self, collection_name="ORG", document_id=None, field_name=None):
        """
        Get the values of a list field from a specific document.

        Args:
        - collection_name (str): The name of the collection.
        - document_id (str): The ID of the document.
        - field_name (str): The name of the list field.

        Returns:
        - list: The values in the list field, or an empty list if the field is not found.
        """
        # Initialize Firestore connection if not already initialized
        if not self.db:
            self.initialize_firestore()

        # Get the reference to the document
        document_ref = self.db.collection(collection_name).document(document_id)

        # Get the document data
        document_data = document_ref.get().to_dict()

        # Get the values of the list field
        list_values = document_data.get(field_name, None)

        # Close Firestore connection after the operation
        self.close_firestore()

        return list_values
