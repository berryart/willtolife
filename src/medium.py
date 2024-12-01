import requests  
import json

# Replace these with your actual Medium integration token and file path  
with open("credentials.json", "r") as c:
  creds = json.load(c)
  MEDIUM_TOKEN = creds["medium"]["token"]
  USER_ID = creds["medium"]["user_id"]

headers = {  
    'Authorization': f'Bearer {MEDIUM_TOKEN}',  
    'Content-Type': 'application/json',  
    'Accept': 'application/json',  
    'host': 'api.medium.com',  
    'Accept-Charset': 'utf-8'  
}  

url = f'https://api.medium.com/v1/users/{USER_ID}/posts'

# Article content and metadata
data = {
    "title": "Test Image111",
    "contentFormat": "markdown",  # Choose 'html', 'markdown', or 'plain'
    # "content": "# Hello World2!\nThis is my first article using the Medium API.\n![Image](files://G:/My%20Drive/Will%20to%20Life/Images/overman_wide.png)",
    # "content": "# Hello World3!\nThis is my first article using the Medium API.\n![Image](https://drive.google.com/thumbnail?id=1061atDgNRacL1oeiCT8pWmsGeI-xdCuM&sz=w1000)",

    "content": "# Hello World3!\nThis is my first article using the Medium API.\n![Image](https://raw.githubusercontent.com/berryart/willtolife/refs/heads/master/images/inanity_as_cause_of_alcoholism.png)",

    "tags": ["python", "api", "medium"],
    "publishStatus": "draft"  # Choose 'public' or 'draft'
}

# Sending the POST request
response = requests.post(url=url, headers=headers, data=json.dumps(data))

print('Status code:', response.status_code)
print('Response:', response.json())