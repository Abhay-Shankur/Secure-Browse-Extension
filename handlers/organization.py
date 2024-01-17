from flask import jsonify

from firebaseoperations.firebase_authentication import sign_up, sign_in, check_authentication
from firebaseoperations.firebase_operations import FirebaseOperations
from handlers.api_handler import ApiHandler
import firebase_admin
from firebase_admin import auth


class Organization:
    def __init__(self, app_name):
        self._uid = None
        # Initialize the Firebase handler
        self.firebaseHandler = FirebaseOperations(app_name=app_name)
        self._apiHandler = ApiHandler()

    def is_logged_in(self):
        return True if self._uid is not None else False

    #     Authenticate Organisation
    def authenticate_org(self, details):
        """
        :param details: {'orgName', 'orgEmail', 'orgPass'}
        """
        # TODO: Write TRY_EXCEPT for each firebaseauth
        try:
            user = auth.get_user_by_email(details['orgEmail'])
            return user.uid
            # return self.login_org(details)
        except Exception as e:
            print(e)
            return self.register_org(details)
        # if not user:

    #       Registering Organization
    def register_org(self, details):
        """
        :param details: {'orgName', 'orgEmail', 'orgPass'}
        """
        try:
            self._uid = sign_up(email=details['orgEmail'], password=details['orgPass'])
            if self._uid is not None:
                # didDoc = self._apiHandler.register_did()
                didDoc = {
                    'did': 'jncjdsnjcnncvnnn'
                }
                details['didDoc'] = didDoc.get('did', '')
                self.firebaseHandler.add_doc(collection_name='ORG', doc=details, doc_id=details['orgEmail'])
                self.firebaseHandler.add_doc(collection_name='DID', doc=didDoc, doc_id=details['didDoc'])
                return self._uid
            else:
                return None
        except Exception as e:
            print(e)
            return None

    #       Login to Organization
    def login_org(self, details):
        """
        :param details: {'orgEmail', 'orgPass'}
        """
        try:
            self._uid = sign_in(email=details.get('orgEmail', ''), password=details.get('orgPass', ''))
            if self._uid is not None:
                return self._uid
            else:
                return None
        except Exception as e:
            print(e)
            return None

    #       Get Current Organization
    def get_org(self):
        return check_authentication(self._uid)

    # #       Add Protected Url to Organization
    #     def add_url(self, url):
    #         org = check_authentication(self._uid)
    #         return self.firebaseHandler.add_value_to_list_field(collection_name="ORG", document_id=org.email, field_name='protectedUrls', new_value=url)
    #
    # #       Get Protected Url to Organization
    #     def get_url(self):
    #         org = check_authentication(self._uid)
    #         return self.firebaseHandler.get_list_field_values(collection_name="ORG", document_id=org.email, field_name='protectedUrls')

    #       Issue Credentials to Organization User
    def issue_credentials(self, subjectTo, credentials):
        cred = self._apiHandler.issue_credentials(subjectDid=subjectTo, issuerDid=self._uid, fields=credentials)
        cred = cred.get('credentialDocument', None)
        # TODO: Make sure to handle VC after creating
        self.firebaseHandler.add_doc(collection_name="Credentials", doc=cred, doc_id=cred['id'])
        return cred['id']

    # #       Get Organization User
    #     def set_user_list(self, userId, orgEmail=None):
    #         if self._uid is not None:
    #             org = check_authentication(self._uid)
    #             return self.firebaseHandler.add_value_to_list_field(document_id=org.email, field_name='linkedUser', new_value=userId)
    #         else:
    #             return self.firebaseHandler.add_value_to_list_field(document_id=orgEmail, field_name='linkedUser', new_value=userId)
    #
    # #       Get Organization User
    #     def get_user_list(self):
    #         org = check_authentication(self._uid)
    #         return self.firebaseHandler.get_list_field_values(document_id=org.email, field_name='linkedUser')

    #       Set List of Values
    def set_list(self, collection, field, value, uid=None, orgEmail=None):
        if uid is not None:
            org = check_authentication(uid)
            print(org.email)
            return self.firebaseHandler.set_value_to_list_field(collection_name=collection, document_id=org.email,
                                                                field_name=field, new_value=value)
        else:
            return self.firebaseHandler.set_value_to_list_field(collection_name=collection, document_id=orgEmail,
                                                                field_name=field, new_value=value)

    #       Get List of Values
    def get_list(self, collection, field, uid=None):
        if uid is not None:
            org = check_authentication(uid)
            return self.firebaseHandler.get_list_field_values(collection_name=collection, document_id=org.email,
                                                              field_name=field)
        else:
            return None

    #       Display Organisation emails
    def get_org_mails(self):
        return self.firebaseHandler.display_document_names(collection_name='ORG')