from flask import jsonify

from firebaseoperations.firebase_authentication import sign_up, sign_in, check_authentication
from firebaseoperations.firebase_operations import FirebaseOperations
from handlers.api_handler import ApiHandler


class Organization:
    def __init__(self, app_name):
        self._uid = None
        # Initialize the Firebase handler
        self.firebaseHandler = FirebaseOperations(app_name=app_name)
        self._apiHandler = ApiHandler()

    def is_logged_in(self):
        return True if self._uid is not None else False

#       Registering Organization
    def register_org(self, details):
        """
        :param details: {'orgName', 'orgEmail', 'orgPass'}
        """
        self._uid = sign_up(email=details['orgEmail'], password=details['orgPass'])
        if self._uid is not None:
            didDoc = self._apiHandler.register_did()
            details['didDoc'] = didDoc.get('did', '')
            self.firebaseHandler.add_doc(collection_name='ORG', doc=details, doc_id=details['orgEmail'])
            self.firebaseHandler.add_doc(collection_name='DID', doc=didDoc, doc_id=self._uid)
            return jsonify({'uid': self._uid})
        else:
            return jsonify({'uid': None})

#       Login to Organization
    def login_org(self, details):
        """
        :param details: {'orgEmail', 'orgPass'}
        """
        self._uid = sign_in(email=details.get('orgEmail', ''), password=details.get('orgPass', ''))
        if self._uid is not None:
            return jsonify({'uid': self._uid})
        else:
            return jsonify({'uid': None})

#       Get Current Organization
    def get_org(self):
        if check_authentication(self._uid):
            return jsonify({'uid': self._uid})
        else:
            return jsonify({'uid': None})

#       Add Protected Url to Organization
    def add_url(self, url):
        org = check_authentication(self._uid)
        return self.firebaseHandler.add_value_to_list_field(collection_name="ORG", document_id=org.email, field_name='protectedUrls', new_value=url)

#       Get Protected Url to Organization
    def get_url(self):
        org = check_authentication(self._uid)
        return self.firebaseHandler.get_list_field_values(collection_name="ORG", document_id=org.email, field_name='protectedUrls')

#       Issue Credentials to Organization User
    def issue_credentials(self, subjectTo, credentials):
        cred = self._apiHandler.issue_credentials(subjectDid=subjectTo, issuerDid=self._uid, fields=credentials)
        cred = cred.get('credentialDocument', None)
        # TODO: Make sure to handle VC after creating
        self.firebaseHandler.add_doc(collection_name="Credentials", doc=cred, doc_id=cred['id'])
        return cred['id']

#       Get Organization User
    def set_user(self, userId, orgEmail=None):
        if self._uid is not None:
            org = check_authentication(self._uid)
            return self.firebaseHandler.add_value_to_list_field(document_id=org.email, field_name='linkedUser', new_value=userId)
        else:
            return self.firebaseHandler.add_value_to_list_field(document_id=orgEmail, field_name='linkedUser', new_value=userId)

#       Get Organization User
    def get_user(self):
        org = check_authentication(self._uid)
        return self.firebaseHandler.get_list_field_values(document_id=org.email, field_name='linkedUser')

