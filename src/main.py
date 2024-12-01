from reader import Reader
from medium import Medium
from instagram import Instapost, PostPublisher


if __name__ == "__main__":
  rdr = Reader()
  story = rdr.get_story("Meaning in Suffering")
  # # Medium
  # mdm = Medium(story)
  # mdm.makepost()

  # Instagram
  # Make images
  inst = Instapost(story)
  inst.makeimages()
  # Make post
