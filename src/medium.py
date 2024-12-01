import requests  
import json

from reader import Story


class Medium:
  def __init__(self, story: Story) -> None:
    self._story = story
    self._medium_token = None
    self._user_id = None
    self._get_credentials()

  def _get_credentials(self):
    with open("credentials.json", "r") as c:
      creds = json.load(c)
      self._medium_token = creds["medium"]["token"]
      self._user_id = creds["medium"]["user_id"]

  def _compose_post(self):
    res = "# " + self._story.title + "\n"
    res += "## " + self._story.subtitle + "\n"
    res += f"![Image](https://github.com/berryart/willtolife/blob/master/images/{self._story.filename}.webp?raw=true)\n"
    res += self._story.quote + "\n"
    res += self._story.quoteauthor + "\n\n"
    res += self._story.body + "\n\n"
    res += self._story.footnote + "\n\n"
    res += "---\n\n"
    res += "[Will to Life](https://willtolife.org)"
    return res

  def makepost(self):
    headers = {  
        'Authorization': f'Bearer {self._medium_token}',  
        'Content-Type': 'application/json',  
        'Accept': 'application/json',  
        'host': 'api.medium.com',  
        'Accept-Charset': 'utf-8'  
    }     
    url = f'https://api.medium.com/v1/users/{self._user_id}/posts'

    # Article content and metadata
    data = {
        "title": self._story.title,
        "contentFormat": "markdown",  # Choose 'html', 'markdown', or 'plain'
        "content": self._compose_post(),
        # "content": "# Hello World3!\nThis is my first article using the Medium API.\n![Image](https://github.com/berryart/willtolife/blob/master/images/inanity_as_cause_of_alcoholism.png?raw=true)",
        "tags": ["sobriety", "recovery", "addiction", "addiction recovery", "alcoholism"],
        "publishStatus": "draft"  # Choose 'public' or 'draft'
    }

    # Sending the POST request
    response = requests.post(url=url, headers=headers, data=json.dumps(data))

    print('Status code:', response.status_code)
    print('Response:', response.json())