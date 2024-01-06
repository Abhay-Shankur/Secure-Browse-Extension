from firebase_admin import firestore


class FirebaseDataConnect():

    def __init__(self):
        # super().__init__()
        # Access Firestore database
        self.db = firestore.client()

    # Function to fetch data from Firebase
    # def fetch_data_from_firebase(self):
    #     # Assuming you have a collection named 'data' and a document with field 'datastring'
    #     # doc_ref = self.db.collection('users').document('your_document_id')
    #     doc_ref = self.db.collection('users')
    #     print(doc_ref)
    #     # data = doc_ref.get().to_dict().get('datastring', '')
    #     # return data

    def get_all_collections(self):
        # Retrieve all collections by listing all documents in the root
        collections = [collection.id for collection in self.db.collections()]
        return collections

    # Function to Add Documents
    def add_doc(self, collection_name="Credentials", doc=None, doc_id=None):
        return self.db.collection(collection_name).document(doc_id).set(doc)

    def get_all_document_fields(self, collection_name="Credentials", document_id=None):
        document_ref = self.db.collection(collection_name).document(document_id)
        document_data = document_ref.get().to_dict()
        return document_data

    def get_all_documents(self, collection_name="Credentials"):
        collection_ref = self.db.collection(collection_name)
        documents = collection_ref.stream()
        return documents

    def display_document_names(self, collection_name="Credentials"):
        all_documents = self.get_all_documents(collection_name=collection_name)
        return [document.id for document in all_documents]
        # for document in all_documents:
        #     print(f"Document ID: {document.id}")

    def get_matching_doc(self, collection_name="Credentials"):
        ref = self.db.collection(collection_name)
        total_doc = ref.get()

        total_count = len(total_doc)
        active_count = sum(1 for doc in total_doc if doc.to_dict().get('age') == 40)
        on_leave_count = sum(1 for doc in total_doc if doc.to_dict().get('age') == 30)

        data = {
            "collection" : collection_name,
            "total": total_count,
            "total-active": active_count,
            "total-onleave": on_leave_count
        }
        return data
        # print(total_count, active_count, on_leave_count)