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
  
  @property
  def narration(self):
    return self.mediapath.joinpath("narration.mp3")
  
  @property
  def captions(self):
    return self.mediapath.joinpath("captions.json")

  @property
  def short(self):
    return self.mediapath.joinpath("short.mp4")
