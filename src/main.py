from reader import Reader
from medium import Medium


if __name__ == "__main__":
  rdr = Reader()
  story = rdr.get_story("Inanity as Cause of Alcoholism")
  mdm = Medium(story)
  mdm.makepost()