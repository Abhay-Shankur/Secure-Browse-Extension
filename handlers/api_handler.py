import time
import requests

from models.sendmail import send_email


class ApiHandler:
    def __init__(self):
        self.url = None
        self.headers = None
        self.params = None
        # Initialize the 'config' attribute
        self.config = {'baseUrl': 'https://api.entity.hypersign.id',
                       'appApi': 'https://ent_7d1d2a9.api.entity.hypersign.id',
                       'apiSecret': '8e160eaf60f98031d2987b236a8e4.c1f5715c66c7effeab03c2074dc96c68522fa28af58b9607eeba37cf902d721817c3afe10485d6e375341a83c4ad1fe55'}
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
            token_type = response_json.get("tokenType", "")
            expires_in = response_json.get("expiresIn", 0)
            self.__commit_access_token(access_token, token_type, expires_in)

        except Exception as error:
            raise error

    # Modify the commit function to add access_token to the config dictionary
    def __commit_access_token(self, access_token, token_type, expires_in):
        self.config['access_token'] = access_token
        self.config['expires_in'] = expires_in
        self.config['tokenType'] = token_type
        self.config['Authorization'] = f'{token_type} {access_token}'
        self.config['expiration_time'] = time.time() + expires_in  # Set the expiration time

    # def get_status(self):
    #     return [self.fb.get_matching_doc(collection_name=collection) for collection in self.fb.get_all_collections()]

    # Creating a DID Document
    def create_did(self):
        self.url = self.config['appApi'] + "/api/v1/did/create"
        self.params = {
            "namespace": "testnet"
        }
        self.headers = {
            'Authorization': self.config['Authorization']
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=self.params)
            # Check the response status code
            if response.status_code == 201 or response.status_code == 200:
                response_json = response.json()
                # self.fb.add_doc(collection_name="DID", doc=response_json, doc_id=response_json.get("did", ""))
                # print(self.fb.add_doc(collection_name="DID", doc=response_json, id=id))
                # send_email(body=fields.get("aadhar", None), to_email=fields.get("email", None))
                # print(response_json)
                # return response_json.get("did", "")
                return response_json
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def register_did(self):
        self.url = self.config['appApi'] + "/api/v1/did/register"
        self.headers = {
            'Authorization': self.config['Authorization']
        }
        # doc_id = self.create_did()
        # doc = self.fb.get_all_document_fields(collection_name="DID", document_id=doc_id)
        doc = self.create_did()
        # TODO: retry until it get
        # for _ in range(3):
        #     doc = self.create_did()
        #     if doc is not None: break
        # while doc is None:
        #     doc = self.create_did()

        self.params = {
            'didDocument': doc['metaData']['didDocument'],
            'verificationMethodId': doc['metaData']['didDocument']["verificationMethod"][0]['id']
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=self.params)
            # Check the response status code
            if response.status_code == 201 or response.status_code == 200:
                response_json = response.json()
                # print(response_json)
                return response_json
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # Issuing Credentials
    def issue_credentials(self,
                          schemaId="sch:hid:testnet:z8451Tv8imAWmBBF8WkV6yCxyfJbBu2Y1yunH4f7zTQC6:1.0",
                          subjectDid=None,
                          issuerDid=None,
                          fields=None):
        self.url = self.config['appApi'] + "/api/v1/credential/issue"
        self.headers = {
            'accept': 'application/json',
            'Authorization': self.config['Authorization']
        }
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
                # print(self.fb.add_cred(cred=response_json, id=fields.get("aadhar",None)))
                # send_email(body=fields.get("aadhar",None),to_email=fields.get("email",None))
                print(response_json)
                return response_json
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
