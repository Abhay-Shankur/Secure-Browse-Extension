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

    def add_value_to_list_field(self, collection_name="ORG", document_id=None, field_name=None, new_value=None):
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

        # Get the reference to the document
        document_ref = self.db.collection(collection_name).document(document_id)

        # Use a transaction to ensure data consistency
        @firestore.transactional
        def update_transaction(transaction, doc_ref, field, value):
            # Get the current state of the document
            doc = transaction.get(doc_ref)

            # Update the set field
            current_set = set(doc.get(field, []))
            current_set.add(value)

            # Update the document with the new list
            transaction.update(doc_ref, {field: list(current_set)})

        try:
            # Run the transaction to update the document
            self.db.run_transaction(update_transaction, document_ref, field_name, new_value)

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
        list_values = document_data.get(field_name, [])

        # Close Firestore connection after the operation
        self.close_firestore()

        return list_values

    def close_connection(self):
        # Stop the listener before closing the connection
        if self.listener:
            self.listener.unsubscribe()

        # Close Firestore connection if not already closed
        self.close_firestore()