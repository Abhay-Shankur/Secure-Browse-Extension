

from firebaseoperations.firebase_authentication import sign_up, sign_in, check_authentication
from firebaseoperations.firebase_operations import FirebaseOperations
from handlers.api_handler import ApiHandler
import firebase_admin
from firebase_admin import auth
import os


script_dir = os.path.dirname(__file__)  # Get the directory of the script
file_path = os.path.join(script_dir, 'create_did.json')


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
            self._uid = user.uid
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
                # Registering New User
                response = self._apiHandler.register_did()
                didDoc = response['metaData']['didDocument']
                details['didDoc'] = response.get('did', '')
                # self.firebaseHandler.add_doc(collection_name='ORG', doc=details, doc_id=details['orgEmail'])
                # self.firebaseHandler.add_doc(collection_name='DID', doc=didDoc, doc_id=details['didDoc'])
                self.firebaseHandler.add_doc(collection_name='ORG', doc=details, doc_id=details['orgEmail'])
                self.firebaseHandler.add_doc(collection_name='DID', doc=didDoc, doc_id=details['didDoc'])
                return self._uid
            else:
                return None
        except Exception as e:
            print('Exception: ', e)
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
    def get_org(self, uid):
        return check_authentication(uid)

    # #       Add Protected Url to Organization
    #     def add_url(self, url):
    #         org = check_authentication(self._uid)
    #         return self.firebaseHandler.add_value_to_list_field(collection_name="ORG", document_id=org.email, field_name='protectedUrls', new_value=url)
    #
    # #       Get Protected Url to Organization
    #     def get_url(self):
    #         org = check_authentication(self._uid)
    #         return self.firebaseHandler.get_list_field_values(collection_name="ORG", document_id=org.email, field_name='protectedUrls')
    # def get_json(self):
    #     data = {
    #       "credentialDocument": {
    #         "@context": [
    #           "https://www.w3.org/2018/credentials/v1",
    #           "https://raw.githubusercontent.com/hypersign-protocol/hypersign-contexts/main/HypersignCredentialStatus2023.jsonld",
    #           {
    #             "@context": {
    #               "@protected": True,
    #               "@version": 1.1,
    #               "id": "@id",
    #               "type": "@type",
    #               "OptiSecure": {
    #                 "@context": {
    #                   "@propagate": True,
    #                   "@protected": True,
    #                   "xsd": "http://www.w3.org/2001/XMLSchema#",
    #                   "username": {
    #                     "@id": "https://hypersign-schema.org/username",
    #                     "@type": "xsd:string"
    #                   },
    #                   "email": {
    #                     "@id": "https://hypersign-schema.org/email",
    #                     "@type": "xsd:string"
    #                   },
    #                   "aadhar": {
    #                     "@id": "https://hypersign-schema.org/aadhar",
    #                     "@type": "xsd:string"
    #                   },
    #                   "dob": {
    #                     "@id": "https://hypersign-schema.org/dob",
    #                     "@type": "xsd:string"
    #                   }
    #                 },
    #                 "@id": "https://hypersign-schema.org"
    #               }
    #             }
    #           },
    #           "https://w3id.org/security/suites/ed25519-2020/v1"
    #         ],
    #         "id": "vc:hid:testnet:z6MkqrdX4uNunPLhMn859siZB4L7xod9nYxqHcpqiJfuK1Kf",
    #         "type": [
    #           "VerifiableCredential",
    #           "OptiSecure"
    #         ],
    #         "expirationDate": "2027-12-10T18:30:00Z",
    #         "issuanceDate": "2024-01-20T12:56:44Z",
    #         "issuer": "did:hid:testnet:z6Mkqneo5wK7YCXkxt7RWJjjxGcRLcee7yEZiiXTeuQmCs7N",
    #         "credentialSubject": {
    #           "username": "user1",
    #           "email": "user1@gmail.com",
    #           "aadhar": "123456789012",
    #           "dob": "21-02-2003",
    #           "id": "did:hid:testnet:z6MkfExumxD1j2nnt4oxoyjAgmJ7SPxjroTkSLnZiziZxt7H"
    #         },
    #         "credentialSchema": {
    #           "id": "sch:hid:testnet:z6Mktq4jx9ELWnuBKWKLYBQd66T1EJGNrrYnn5wK2QHuhaht:1.0",
    #           "type": "JsonSchemaValidator2018"
    #         },
    #         "credentialStatus": {
    #           "id": "https://api.prajna.hypersign.id/hypersign-protocol/hidnode/ssi/credential/vc:hid:testnet:z6MkqrdX4uNunPLhMn859siZB4L7xod9nYxqHcpqiJfuK1Kf",
    #           "type": "HypersignCredentialStatus2023"
    #         },
    #         "proof": {
    #           "type": "Ed25519Signature2020",
    #           "created": "2024-01-20T12:58:25Z",
    #           "verificationMethod": "did:hid:testnet:z6Mkqneo5wK7YCXkxt7RWJjjxGcRLcee7yEZiiXTeuQmCs7N#key-1",
    #           "proofPurpose": "assertionMethod",
    #           "proofValue": "z5eRP6ShHrYkBq2iAT21C22ha1Yr5DV2x1DcahiBpmVa1E7RnGzEKS8yng6PHBf3VY27XorTaNhaAVNHnt2vQCTQZ"
    #         }
    #       },
    #       "credentialStatus": {
    #         "@context": [
    #           "https://raw.githubusercontent.com/hypersign-protocol/hypersign-contexts/main/CredentialStatus.jsonld",
    #           "https://w3id.org/security/suites/ed25519-2020/v1"
    #         ],
    #         "id": "vc:hid:testnet:z6MkqrdX4uNunPLhMn859siZB4L7xod9nYxqHcpqiJfuK1Kf",
    #         "issuer": "did:hid:testnet:z6Mkqneo5wK7YCXkxt7RWJjjxGcRLcee7yEZiiXTeuQmCs7N",
    #         "issuanceDate": "2024-01-20T12:56:44Z",
    #         "remarks": "Credential is active",
    #         "credentialMerkleRootHash": "44e3bc69effc4b348428fb961f01a089d54c4785516db4b52b90a252a5149c0d",
    #         "proof": {
    #           "type": "Ed25519Signature2020",
    #           "created": "2024-01-20T12:58:25Z",
    #           "verificationMethod": "did:hid:testnet:z6Mkqneo5wK7YCXkxt7RWJjjxGcRLcee7yEZiiXTeuQmCs7N#key-1",
    #           "proofPurpose": "assertionMethod",
    #           "proofValue": "zBZ8oV2n6ius28i9cyN8RcHvPPVnPpDaFh16G8UZ5b9QtT8J9JsTANbtRAckQ1e7AzSc7j48VoxPA2K7dLemuyLV"
    #         }
    #       },
    #       "persist": True
    #     }
    #     return data

    #       Issue Credentials to Organization User
    def issue_credentials(self, subjectTo, credentials, uid=None):
        try:
            issuer = self.get_org(uid).email
            docs = self.firebaseHandler.get_all_document_fields(collection_name='ORG', document_id=issuer)
            receiverDid = docs['users'][subjectTo]['did']
            # receiver = self.firebaseHandler.get_all_document_fields(collection_name='USER', document_id=subjectTo)
            print(f"Sender: {docs['didDoc']}")
            print(f"Receiver: {receiverDid}")
            cred = self._apiHandler.issue_credentials(subjectDid=receiverDid, issuerDid=docs['didDoc'], fields=credentials)

            # TODO Get mail of user.
            # TODO: Make sure to handle VC after creating
            self.firebaseHandler.add_doc(collection_name="Credentials", doc=cred, doc_id=cred['credentialDocument']['id'])
            self.firebaseHandler.set_value_to_list_field(collection_name='USER',document_id=subjectTo,field_name='credentials',new_value=cred['credentialDocument']['id'])
            # self.firebaseHandler.add_doc(collection_name="Credentials", doc=json_data, doc_id=json_data['credentialDocument']['id'])
            # self.firebaseHandler.set_value_to_list_field(collection_name='USER', document_id=subjectTo, field_name='credentials', new_value=json_data['credentialDocument']['id'])
            return True
        except Exception as e:
            print(e)
            return False
        # self.firebaseHandler
        # return cred['id']

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
