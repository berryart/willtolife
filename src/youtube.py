import json
import os
import whisper
from moviepy import ImageClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx import Resize, Scroll
from PIL import Image
import math
import numpy

from config import Config

W = 540
H = 960
CLIP_DURATION = 5

class Short:
  def __init__(self, title):
    self.narrative_file_path = title
    self.title = "Amor Fati as Beginning"

  def generate_captions(self):
    model = whisper.load_model("base")
    result = model.transcribe(
      self.narrative_file_path,
      word_timestamps=True,
    )
    
    res = []
    for s in result["segments"]:
        res += s["words"]

    words = []
    for w in res:
        words.append({
            "word": w["word"],
            "start": float(w["start"]),
            "end": float(w["end"]),
        })

    with open("data.json", "w") as outfile:
      json.dump(words, outfile)
    
    return words
  
  def _get_image_paths(self):
     contents = os.listdir(Config.src_image_path)
     return [f"./images/{i}" for i in contents]

  def _zoom_in_effect(self, ipath, n, zoom_ratio=0.04):
    clip = ImageClip(ipath, duration=CLIP_DURATION)
    clip = clip.with_effects([Resize(height=H)])
    
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    clip = clip.with_start(CLIP_DURATION * n).with_position(("center", "center"))
    return clip.transform(effect)
  
  def _subgen(self, text):
      res = TextClip(
          "./fonts/LibreBaskerville-Bold.ttf", 
          text=text, 
          size=(W, 35),
          color='white',
          stroke_color="black", 
          stroke_width=2,
          interline=20,
          text_align="center", 
          method='caption',
          margin=(0, 700),
      )
      # res = TextClip(
      #     "./fonts/LibreBaskerville-Bold.ttf", 
      #     text=text, 
      #     # font_size=24,
      #     color="white",
      #     bg_color="black",
      #     size=(W, 25),
      #     method="caption",
      # )      
      # res = res.with_position((0, "bottom"))
      return res

  def _wrap_text(self, text, charlimit):
    res = ""
    row = ""
    words = text.split(" ")

    for w in words:
      wordlen = len(w)
      rowlen = len(row)
      if rowlen + wordlen <= charlimit:
        row += w + " "
      else:
        res += row + "\n" + w + " "
        row = ""
    
    res += row
    res = res.replace("\\", "")
    return res
  
  def compose(self):
    narration = AudioFileClip(self.narrative_file_path)
    images = self._get_image_paths()
    imageclips = [self._zoom_in_effect(i, n) for n, i in enumerate(images)]

    subs = []
    with open("./media/amor_fati_as_beginning/captions.json", "r", encoding="utf-8") as s:
        rawsubs = json.load(s)
        for rs in rawsubs:
            subs.append(((rs["start"], rs["end"]), rs["word"]))
    subtitles = SubtitlesClip(subs, make_textclip=self._subgen)
    imageclips.append(subtitles)

    title_text = self._wrap_text(self.title, 17)
    title = TextClip(
        "./fonts/LibreBaskerville-Bold.ttf", 
        text=title_text, 
        font_size=50,
        color="white",
        margin=(25, 25, 25, 25)
    )
    imageclips.append(title)

    output = CompositeVideoClip(imageclips, size=(W, H))
    output.audio = narration
    output.duration = narration.duration
    output.write_videofile("./media/amor_fati_as_beginning/short.mp4", fps=30)

if __name__ == "__main__":
  s = Short("./media/amor_fati_as_beginning/narration.mp3")
  #  s.generate_captions()
  s.compose()
