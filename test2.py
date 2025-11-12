# import requests

# url = "https://api.d-id.com/agents/client-key"

# payload = { "allowed_domains": ["Hello world"] }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authorization": "Basic WW1GdWEzQnliMk52YVc1QVoyMWhhV3d1WTI5dDpUNVdtbFRRWXdCcFExTmxUQnkxN2s="
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)


import requests

url = "https://api.d-id.com/agents/client-key"

headers = {
    "accept": "application/json",
    "authorization": "Basic WW1GdWEzQnliMk52YVc1QVoyMWhhV3d1WTI5dDpUNVdtbFRRWXdCcFExTmxUQnkxN2s="
}

response = requests.get(url, headers=headers)

print(response.text)