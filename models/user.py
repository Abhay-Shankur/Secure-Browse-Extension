import requests


class User:
    def create_did(self):
        url = self.config['baseUrl'] + "/api/v1/did/create"
        headers = {
            'accept': 'application/json',
            'Authorization': self.config['Authorization']
        }
        data = {
            "namespace": "testnet",
        }
        try:
            response = requests.post(url, headers=headers, data=data)

            # Check the response status code
            if response.status_code == 200:
                response_json = response.json()
                return response_json.get("did", "")
                # db = HypersignDatabase()
                # db.insert_data(response_json.get("did", ""), response_json.get("registrationStatus", ""))
            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)

        except Exception as e:
            print(f"An error occurred: {e}")

    def register_did(self, did=None):
        url = self.config['baseUrl'] + "/api/v1/did/register"
        headers = {
            'accept': 'application/json',
            'Authorization': self.config['Authorization']
        }
        # doc = self.get_did(did=did)
        doc = self.create_did()
        params = {
            'didDocument': doc,
            'verificationMethodId': doc.get("capabilityDelegation",{})[0]
        }
        # print(params)
        try:
            response = requests.post(url, headers=headers, json=params)

            # Check the response status code
            if response.status_code == 200:
                response_json = response.json()
                print(response_json)
                # for hid in response_json.get("data", []):
                #     self.get_hid(hid=hid)

            else:
                print(f"Error: {response.status_code}")
                print("Error Response:", response.text)

        except Exception as e:
            print(f"An error occurred: {e}")
