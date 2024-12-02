import json
import praw

from reader import Story
from chatgpt import OpenAI


class Reddit:
  def __init__(self) -> None:
    with open("credentials.json", "r") as c:
      creds = json.load(c)
      self.client = praw.Reddit(
          client_id=creds["reddit"]["client_id"],
          client_secret=creds["reddit"]["client_secret"],
          user_agent=creds["reddit"]["user_agent"],
          username=creds["reddit"]["username"],
          password=creds["reddit"]["password"],
      )

  def makepost(self, story: Story):
    ai = OpenAI()
    body = ai.personalize_text(story.body + "\n\n" + story.footnote)

    title = story.title
    text =  story.quote + "\n" + \
            story.quoteauthor + "\n\n" + \
            body + "\n\n" + \
            "P.S.: I can do it, so can you. Check my profile for other reflections about recovery."

    print(text)

    # Submit the post
    subreddit_name = "willtolife"  # Change to your desired subreddit
    subreddit = self.client.subreddit(subreddit_name)
    subreddit.submit(title=title, selftext=text)
    print(f"Posted to Reddit: {title}")