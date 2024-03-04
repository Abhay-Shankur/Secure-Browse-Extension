import json
import time
import requests

from models.sendmail import send_email


class ApiHandler:
    def __init__(self):
        self.url = None
        self.headers = None
        self.params = None
        # Initialize the 'config' attribute
        self.config = {'baseUrl': 'https://api.entity.dashboard.hypersign.id',
                       'appApi': 'https://ent-27e3656.api.entity.hypersign.id',
                       'apiSecret': '137cbaf5df879c434cba0ea48402c.6abbad0bd95fe918a60e6540403d4f93b253bcd074137938f7f78ad00b3223774c070a01e99c6495013ec1397fdb63565'}
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
            # print(self.config)

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

    # Get all DID Document

    # Creating a DID Document
    def create_did(self):
        self.url = self.config['appApi'] + "/api/v1/did/create"
        self.params = {
            "namespace": "testnet"
        }
        self.headers = {
            "accept": "application/json",
            'Content-Type': 'application/json',
            'Authorization': self.config['Authorization'],
            'origin': '*'
        }
        try:

            response = requests.post(self.url, headers=self.headers, json=self.params)
            # Check the response status code
            if response.status_code == 201 or response.status_code == 200:
                response_json = response.json()
                # self.fb.add_doc(collection_name="DID", doc=response_json, doc_id=response_json.get("did", ""))
                # print(self.fb.add_doc(collection_name="DID", doc=response_json, id=id))
                # send_email(body=fields.get("aadhar", None), to_email=fields.get("email", None))
                print('Created DID:',response_json)
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
        doc = self.create_did()

        self.url = self.config['appApi'] + "/api/v1/did/register"
        self.headers = {
            'accept': 'application/json',
            "Content-Type": "application/json",
            'Authorization': self.config['Authorization'],
            'origin': '*'
        }

        # TODO: retry until it get
        # for _ in range(3):
        #     doc = self.create_did()
        #     if doc is not None: break
        # while doc is None:
        #     doc = self.create_did()

        # TODO: From HyperSign
        self.params = {
            'didDocument': doc['metaData']['didDocument'],
            'verificationMethodId': doc['metaData']['didDocument']["verificationMethod"][0]['id']
        }

        # Assuming your JSON file is named 'your_file.json'
        # with open('create_json', 'r') as file:
        #     json_data = json.load(file)

        # self.params = {
        #     'didDocument': json_data,
        #     'verificationMethodId': json_data["verificationMethod"][0]['id']
        # }
        try:
            # print(self.url)
            # print(self.headers)
            # print(self.params)

            response = requests.post(self.url, headers=self.headers, json=self.params)
            # Check the response status code
            if response.status_code == 201 or response.status_code == 200:
                response_json = response.json()
                # print(response_json)
                return response_json
                # return response_json['did']
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # Issuing Credentials
    def issue_credentials(self,
                          schemaId="sch:hid:testnet:z6Mko3T2WLHx9yXM8ddPJbYFehnzXTc6hf7y8VmeQBYANPL5:1.0",
                          subjectDid=None,
                          issuerDid=None,
                          fields=None):

        # {
        #     "schemaId": "sch:hid:testnet:z6Mko3T2WLHx9yXM8ddPJbYFehnzXTc6hf7y8VmeQBYANPL5:1.0",
        #     "transactionHash": "A14252A8E6B12DEF8DB596FCEE1EA8353E92565FC51D01FECD9792E93F8FA93F"
        # }
        self.url = self.config['appApi'] + "/api/v1/credential/issue"
        self.headers = {
            'accept': 'application/json',
            "Content-Type": "application/json",
            'Authorization': self.config['Authorization'],
            'origin': '*'
        }
        self.params = {
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

#
# api = ApiHandler()
# # api = api.create_did()
# api.register_did()