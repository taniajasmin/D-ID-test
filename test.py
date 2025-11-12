import base64, requests

DID_KEY = "YmFua3Byb2NvaW5AZ21haWwuY29t:T5WmlTQYwBpQ1NlTBy17k"
auth = base64.b64encode(DID_KEY.encode("ascii")).decode("ascii")
headers = {
    "Authorization": f"Basic {auth}",
    "accept": "application/json"
}

res = requests.get("https://api.d-id.com/talks", headers=headers)
print(res.status_code, res.text)
