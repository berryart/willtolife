import os
from pathlib import Path


class IO:
  def __init__(self, story):
    self.story = story
    self.mediapath = Path(f'./media/{self.story.lower().replace(" ", "_").replace("'", "")}')
    os.makedirs(self.mediapath, exist_ok=True)
  
  @property
  def script(self):
    return self.mediapath.joinpath("script.md")