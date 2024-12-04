import json
import whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

def generate_captions(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(
      video_path,
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
    return words

def add_captions_to_video(video_path, captions):
    video = VideoFileClip(video_path)
    text_clip = TextClip(captions, fontsize=24, color='white')
    text_clip = text_clip.set_position(('center', 'bottom'))
    final_video = CompositeVideoClip([video, text_clip])
    final_video.write_videofile("output_video.mp4")

def subgen(text):
    return TextClip(
        "./fonts/LibreBaskerville-Bold.ttf", 
        text=text, 
        # font_size=24, 
        size=(480, 25),
        color='white', 
        interline=10,
        text_align="center", 
        method='caption',
        margin=(0, 300),
        # horizontal_align="center",
        # vertical_align="bottom",
    ).with_position(0, 200)

def caps(video_path):
  subs = []
  with open("./subs/recovery_and_naturalized_spirituality_quote.json", "r", encoding="utf-8") as s:
      rawsubs = json.load(s)
      for rs in rawsubs["subs"]:
          subs.append(((rs["start"], rs["end"]), rs["word"]))

  subtitles = SubtitlesClip(subs, make_textclip=subgen)
  video = VideoFileClip(video_path)
  result = CompositeVideoClip([video, subtitles])
  result.write_videofile("output.mp4")
  result.audio.write_audiofile("output.mp3")
                       
if __name__ == "__main__":
    video_path = "C:/Users/Valued Customer/Downloads/video.mp4"
    # captions = generate_captions(video_path)
    # print(captions)
    caps(video_path)
    