import json
import os
from pathlib import Path
import whisper
from moviepy import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx import Resize, FadeOut
from moviepy.audio.fx import MultiplyVolume, AudioFadeOut
from PIL import Image
import math
import numpy

from content_io import IO
from config import Config
from reader import Story

W = 540
H = 960
CLIP_DURATION = 5

class Short:
  def __init__(self, story: Story):
    # self.narrative_file_path = title
    # self.title = "Amor Fati as Beginning"
    self.story = story
    self.io = IO(story.title)

  def generate_captions(self):
    if Path.exists(self.io.captions):
       print("Captions already exists! Skipping...")
       return
    if not Path.exists(self.io.narration):
       print("Narration is not found!")
       return
    
    model = whisper.load_model("base")
    result = model.transcribe(
      str(self.io.narration),
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

    with open(self.io.captions, "w") as outfile:
      json.dump(words, outfile)
    
    return words
  
  def _get_image_paths(self):
     contents = os.listdir(Config.src_image_path)
     return [f"{Config.src_image_path}/{i}" for i in contents]

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
    if not Path.exists(self.io.captions):
       print(f"Captions not found at: {self.io.captions}")
       return
    
    music = AudioFileClip(Config.music_echoofsaddness)
    music = music.with_effects([MultiplyVolume(0.15), AudioFadeOut(0.5)])

    narration = AudioFileClip(self.io.narration)
    music = music.subclipped(46.0, 46.0 + narration.duration + 1)
    narration = narration.with_effects([MultiplyVolume(2.0)])
    narration = narration.with_effects([AudioFadeOut(0.5)])

    images = self._get_image_paths()
    imageclips = [self._zoom_in_effect(i, n) for n, i in enumerate(images)]

    subs = []
    with open(self.io.captions, "r", encoding="utf-8") as s:
        rawsubs = json.load(s)
        for rs in rawsubs:
            subs.append(((rs["start"], rs["end"]), rs["word"]))
    subtitles = SubtitlesClip(subs, make_textclip=self._subgen)
    imageclips.append(subtitles)

    # Title
    title_text = self._wrap_text(self.story.title, 17)
    title = TextClip(
        "./fonts/LibreBaskerville-Bold.ttf", 
        text=title_text, 
        font_size=50,
        color="white",
        bg_color=(0, 0, 0, 100),
        margin=(25, 25, 25, 25)
    )
    title = title.with_position((0, 100))
    title = title.with_duration(3)
    imageclips.append(title)

    # Subtitle
    subtitle_text = self._wrap_text(self.story.subtitle, 20)
    subtitle = TextClip(
        "./fonts/LibreBaskerville-Regular.ttf", 
        text=subtitle_text, 
        font_size=35,
        color="white",
        bg_color=(0, 0, 0, 50),
        margin=(25, 25, 25, 25)
    )
    subtitle = subtitle.with_position((0, 100 + title.size[1]))
    subtitle = subtitle.with_duration(3)
    imageclips.append(subtitle)

    output = CompositeVideoClip(imageclips, size=(W, H))
    output = output.with_effects([FadeOut(1.0)])
    audio = CompositeAudioClip([music, narration])
    output.audio = audio
    output.duration = narration.duration + 1
    output.write_videofile(self.io.short, fps=30)

