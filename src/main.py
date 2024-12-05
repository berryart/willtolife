from pathlib import Path
import sys

from reader import Reader
from medium import Medium
from reddit import Reddit
from instagram import Instapost, PostPublisher, StoryPublisher
from youtube import Short


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
  elif engine == "-ic":
    # Make Instagram images
    story = rdr.readscript()
    inst = Instapost(story)
    inst.makeimages()
  elif engine == "-ip":
    # Make post
    story = rdr.readscript()
    post = PostPublisher(story)
    post.publish()
  elif engine == "-is":
    # Make post
    story = rdr.readscript()
    post = StoryPublisher(story)
    post.publish()    
  elif engine == "-yc":
    story = rdr.readscript()
    short = Short(story)
    short.generate_captions()
    short.compose()

  # # Reddit
  # rdr = Reddit()
  # text = rdr.makepost(story)
  else:
    raise Exception(f"Unknown flag: {engine}")