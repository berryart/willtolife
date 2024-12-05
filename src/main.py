import sys

from reader import Reader
from medium import Medium
from reddit import Reddit
from instagram import Instapost, PostPublisher


if __name__ == "__main__":
  title = sys.argv[1]
  engine = sys.argv[2]

  rdr = Reader(title)

  # Script
  if engine == "-s":
    story = rdr.makescript()
  elif engine == "-m":
    # Medium
    story = rdr.readscript()
    mdm = Medium(story)
    mdm.makepost()

  # # Instagram
  # # Make images
  # inst = Instapost(story)
  # inst.makeimages()
  # # Make post
  # post = PostPublisher(story)
  # post.makepost()

  # # Reddit
  # rdr = Reddit()
  # text = rdr.makepost(story)