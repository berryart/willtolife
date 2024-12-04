from moviepy import ImageSequenceClip, ImageClip, VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx import Resize, Scroll
from PIL import Image
import math
import numpy

W = 1080
H = 1920
S = 0.5

SIZE = (int(W*S), int(H*S))
FRAME = 0.0

def getpos(t):
  global FRAME
  FRAME += 1
  return (-t*10, -t*10)

def create_image(ipath, n, d):
  slide = ImageClip(ipath, duration=5)
  slide = slide.with_effects([Resize(height=int(H*S))]) # height computed automatically.
  # slide = slide.with_effects([Resize(lambda t: 1 + 0.02 * t)]) # slow clip swelling
  # slide = slide.with_effects([Scroll(y_speed=-15)]) # slow clip swelling
  # slide = slide.with_effects([Resize(lambda t: 1 + 0.02 * t)]) # slow clip swelling
  # slide = slide.with_position(getpos)
  # slide = slide.with_position(lambda t: (-0.02*t, -0.02*t))
  slide = slide.with_start(5 * n)
  
  return slide

def zoom_in_effect(ipath, n, zoom_ratio=0.04):
    clip = ImageClip(ipath, duration=5)
    clip = clip.with_effects([Resize(height=int(H*S))]) # height computed automatically.
    
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

    clip = clip.with_start(5 * n).with_position(("center", "center"))
    return clip.transform(effect)

def compose_story():
  narration = AudioFileClip("output.mp3")
  images = [
    "./images/inanity_as_cause_of_alcoholism.webp",
    "./images/meaning_in_suffering.webp",
    "./images/recovery_and_naturalized_spirituality.webp",
  ]
  # imageclips = [create_image(i, n, narration.duration) for n, i in enumerate(images)]
  imageclips = [zoom_in_effect(i, n) for n, i in enumerate(images)]

  # img = ImageSequenceClip(images, durations=[narration.duration/3, narration.duration/3, narration.duration/3])
  # output = CompositeVideoClip([img.with_effects([Resize((460, 560))])], size=(480, 560))
  
  output = CompositeVideoClip(imageclips, size=SIZE)
  output.audio = narration
  output.duration = narration.duration
  output.write_videofile("story.mp4", fps=30)


if __name__ == "__main__":
  compose_story()