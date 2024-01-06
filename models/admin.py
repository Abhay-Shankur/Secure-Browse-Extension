import time

import requests

from firebaseoperations.firestore_database import FirebaseDataConnect
from models.sendmail import send_email


class Admin:
    def __init__(self):
        self.url = None
        self.headers = None
        self.params = None
        # Initialize the Firebase handler
        self.fd = FirebaseDataConnect()
        # Initialize the 'config' attribute
        self.config = {'baseUrl': 'https://api.entity.hypersign.id',
                       'apiSecret': '1fc7504b27223b6b0b350c346d91a.437595754a8f3adf8cb85ae7dcbd34d89735fdc5eaf8547148c4e5512549dfdca443e46aee506def00f1565eeef7a7d23'}
        # Assuming that config is a dictionary containing 'baseUrl' and 'apiSecret'
        self.__authenticate_entity()

    def __authenticate_entity(self):
        try:
            self.url = self.config['baseUrl'] + "/api/v1/app/oauth"
            self.headers = {
                "Content-Type": "application/json",
                "X-Api-Secret-Key": self.config['apiSecret'],
            }

            response = requests.post(self.url, headers=self.headers, data='')
            response_json = response.json()

            if response.status_code == 400:
                raise Exception("Bad Request" + response_json.get("message", ""))
            elif response.status_code == 401:
                raise Exception("Invalid API Secret Key")
            elif response.status_code != 200:
                print("Connection Failed")

            access_token = response_json.get("access_token", "")
            expires_in = response_json.get("expiresIn", 0)
            self.__commit_access_token(access_token, expires_in)

        except Exception as error:
            raise error

    # Modify the commit function to add access_token to the config dictionary
    def __commit_access_token(self, access_token, expires_in):
        self.config['access_token'] = access_token
        self.config['expires_in'] = expires_in
        self.config['token_type'] = 'Bearer'
        self.config['Authorization'] = f'Bearer {access_token}'
        self.config['expiration_time'] = time.time() + expires_in  # Set the expiration time

    def get_status(self):
        return [self.fd.get_matching_doc(collection_name=collection) for collection in self.fd.get_all_collections()]

    # Issuing Credentials
    def issue_credentials(self,schemaId="sch:hid:testnet:z8451Tv8imAWmBBF8WkV6yCxyfJbBu2Y1yunH4f7zTQC6:1.0",subjectDid=None,issuerDid="did:hid:testnet:zC4kuoGGUDJDmzk5H97YNmQdzr8K3kF4qfjWFs3Ap86f6",fields=None):
        self.url = self.config['baseUrl'] + "/api/v1/credential/issue"
        # headers = {
        #     'accept': 'application/json',
        #     'Authorization': self.config['Authorization']
        # }
        self.params ={
            "schemaId": schemaId,
            "subjectDid": subjectDid,
            "issuerDid": issuerDid,
            "expirationDate": "2027-12-10T18:30:00.000Z",
            "fields": fields,
            "namespace": "testnet",
            "verificationMethodId": f"{issuerDid}#key-1",
            "persist": True,
            "registerCredentialStatus": True
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=self.params)
            # Check the response status code
            if response.status_code == 201:
                response_json = response.json()
                print(self.fd.add_cred(cred=response_json, id=fields.get("aadhar",None)))
                send_email(body=fields.get("aadhar",None),to_email=fields.get("email",None))
                print(response_json)
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_did(self):
        self.url = self.config['baseUrl'] + "/api/v1/did/create"
        # headers = {
        #     'accept': 'application/json',
        #     'Authorization': self.config['Authorization']
        # }
        self.params = {
            "namespace": "testnet"
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=self.params)
            # Check the response status code
            if response.status_code == 201:
                response_json = response.json()
                self.fd.add_doc(collection_name="DID", doc=response_json, doc_id=response_json.get("did", ""))
                # print(self.fd.add_doc(collection_name="DID", doc=response_json, id=id))
                # send_email(body=fields.get("aadhar", None), to_email=fields.get("email", None))
                print(response_json)
                return response_json.get("did", "")
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)
        except Exception as e:
            print(f"An error occurred: {e}")

    def register_did(self):
        self.url = self.config['baseUrl'] + "/api/v1/did/register"
        doc_id = self.create_did()
        doc = self.fd.get_all_document_fields(collection_name="DID", document_id=doc_id)
        self.params = {
            'didDocument': doc,
            'verificationMethodId': doc.get("capabilityDelegation", {})[0]
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=self.params)
            # Check the response status code
            if response.status_code == 200:
                response_json = response.json()
                print(response_json)
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)
        except Exception as e:
            print(f"An error occurred: {e}")
