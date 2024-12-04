from reader import Reader
from medium import Medium
from reddit import Reddit
from instagram import Instapost, PostPublisher


if __name__ == "__main__":
  rdr = Reader()
  story = rdr.get_story("Three Meanings in Life")
  # # Medium
  # mdm = Medium(story)
  # mdm.makepost()

  # Instagram
  # Make images
  inst = Instapost(story)
  inst.makeimages()
  # # Make post
  # post = PostPublisher(story)
  # post.makepost()

  # # Reddit
  # rdr = Reddit()
  # text = rdr.makepost(story)