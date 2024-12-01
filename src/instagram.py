import json
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont

import config
from reader import Story


class Instapost:
  post_size = 1024
  badge_height = 650
  quote_top = 250
  quote_width = 40
  body_width = 45
  margin = 30

  text_color = "black"
  reg_font_path = "./fonts/LibreBaskerville-Regular.ttf"
  bold_font_path = "./fonts/LibreBaskerville-Bold.ttf"
  itl_font_path = "./fonts/LibreBaskerville-Italic.ttf"
  quote_font_path = "./fonts/SortsMillGoudy-Regular.ttf"

  h1_font_size = 54
  h2_font_size = 34
  reg_font_size = 34
  font_spacing = 20
  
  def __init__(self, story: Story) -> None:
    self.story = story

  def makeimages(self):
    self._make_cover()
    self._make_quote()
    self._make_body()

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
    return res
  
  def _make_body(self):
    image_path = f"{config.Config.src_image_path}{self.story.filename}.webp"
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    top_left = (0, 0)
    bottom_right = (Instapost.post_size, Instapost.post_size)
    fill_color = "white"
    draw.rectangle([top_left, bottom_right], fill=fill_color)

    # Body
    font = ImageFont.truetype(Instapost.reg_font_path, size=Instapost.reg_font_size)
    text = self._wrap_text(self.story.body, Instapost.body_width)
    text = text.replace("*", "").replace("\\", "")
    text_x = Instapost.margin
    text_y = Instapost.margin
    text_position = (text_x, text_y)
    draw.text(text_position, text, font=font, fill=Instapost.text_color, spacing=Instapost.font_spacing)

    # Swipe left
    font = ImageFont.truetype(Instapost.reg_font_path, size=Instapost.reg_font_size)
    text_rect = draw.textbbox((0, 0), "(swipe left)", font=font)
    text_width = text_rect[2] - text_rect[0]
    text_x = Instapost.post_size / 2 - text_width / 2
    text_y = Instapost.post_size - 50
    text_position = (text_x, text_y)
    draw.text(text_position, "(swipe left)", font=font, fill="grey", spacing=Instapost.font_spacing)

    image.save(f"{config.Config.dst_image_path}{self.story.filename}_body.jpeg")

  def _make_quote(self):
    image_path = f"{config.Config.src_image_path}{self.story.filename}.webp"
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    top_left = (0, 0)
    bottom_right = (Instapost.post_size, Instapost.post_size)
    fill_color = "white"
    draw.rectangle([top_left, bottom_right], fill=fill_color)

    # Qute sign
    font = ImageFont.truetype(Instapost.quote_font_path, size=300)
    text_position = (Instapost.post_size / 2 - 75, 20)
    draw.text(text_position, "\"", font=font, fill="grey")

    # Quote
    font = ImageFont.truetype(Instapost.itl_font_path, size=Instapost.reg_font_size)
    text = self._wrap_text(self.story.quote, Instapost.quote_width)
    text += "\n" + self.story.quoteauthor
    text = text.replace("*", "")

    text_rect = draw.textbbox((0, 0), text, font=font)
    text_width = text_rect[2] - text_rect[0]
    text_height = text_rect[3] - text_rect[1]
    text_x = Instapost.post_size / 2 - text_width / 2
    text_y = Instapost.quote_top
    text_position = (text_x, text_y)
    draw.text(text_position, text, font=font, fill=Instapost.text_color, spacing=Instapost.font_spacing)

    # Footnote
    font = ImageFont.truetype(Instapost.reg_font_path, size=Instapost.reg_font_size)
    text = self._wrap_text(self.story.footnote, Instapost.quote_width)
    
    text_rect = draw.textbbox((0, 0), text, font=font)
    text_width = text_rect[2] - text_rect[0]
    text_x = Instapost.post_size / 2 - text_width / 2
    text_y = Instapost.quote_top + text_height + 200
    text_position = (text_x, text_y)
    draw.text(text_position, text, font=font, fill=Instapost.text_color, spacing=Instapost.font_spacing)

    # Swipe left
    font = ImageFont.truetype(Instapost.reg_font_path, size=Instapost.reg_font_size)
    text_rect = draw.textbbox((0, 0), "(swipe left)", font=font)
    text_width = text_rect[2] - text_rect[0]
    text_x = Instapost.post_size / 2 - text_width / 2
    text_y = Instapost.post_size - 50
    text_position = (text_x, text_y)
    draw.text(text_position, "(swipe left)", font=font, fill="grey", spacing=Instapost.font_spacing)

    image.save(f"{config.Config.dst_image_path}{self.story.filename}_quote.jpeg")

  def _make_cover(self):
    image_path = f"{config.Config.src_image_path}{self.story.filename}.webp"
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    top_left = (0, Instapost.badge_height)
    bottom_right = (Instapost.post_size, Instapost.post_size)
    fill_color = "white"
    draw.rectangle([top_left, bottom_right], fill=fill_color)

    # Title
    title_font = ImageFont.truetype(Instapost.bold_font_path, size=Instapost.h1_font_size)
    text_rect = draw.textbbox((0, 0), self.story.title, font=title_font)
    text_width = text_rect[2] - text_rect[0]
    text_height = text_rect[3] - text_rect[1]
    text_x = Instapost.post_size / 2 - text_width / 2
    text_y = Instapost.badge_height + 50
    text_position = (text_x, text_y)
    draw.text(text_position, self.story.title, font=title_font, fill=Instapost.text_color)

    # Subtitle
    title_font = ImageFont.truetype(Instapost.reg_font_path, size=Instapost.h2_font_size)
    text_rect = draw.textbbox((0, 0), self.story.subtitle, font=title_font)
    text_width = text_rect[2] - text_rect[0]
    text_x = Instapost.post_size / 2 - text_width / 2
    text_y = Instapost.badge_height + text_height + 100
    text_position = (text_x, text_y)
    draw.text(text_position, self.story.subtitle, font=title_font, fill=Instapost.text_color)

    # Swipe left
    title_font = ImageFont.truetype(Instapost.reg_font_path, size=Instapost.reg_font_size)
    text_rect = draw.textbbox((0, 0), "(swipe left)", font=title_font)
    text_width = text_rect[2] - text_rect[0]
    text_x = Instapost.post_size / 2 - text_width / 2
    text_y = Instapost.post_size - 50
    text_position = (text_x, text_y)
    draw.text(text_position, "(swipe left)", font=title_font, fill="grey")

    image.save(f"{config.Config.dst_image_path}{self.story.filename}_cover.jpeg")


class PostPublisher:
  def __init__(self, story: Story) -> None:
    self.story = story

  def makepost(self) -> None:
    user = None
    password = None
    with open("credentials.json", "r") as c:
      creds = json.load(c)
      user = creds["instagram"]["user"]
      password = creds["instagram"]["password"]

    cl = Client()
    cl.login(user, password)
    user_id = cl.user_id_from_username(user)
    tags = "#willtolife #stopdrinking #alcoholfree #addiction #addictionrecovery #recovery #quitdrinking #alcoholic #sobrietybooks #AA #alcoholicsanonymous #12sets #sobrietyquotes #philosophy #psychology #positivepsycology #wisdom #growthmindset #motivation #selfimprovement #strength #spiritualreading #support"
    media = cl.album_upload(
        [
          f"{config.Config.dst_image_path}{self.story.filename}_cover.jpeg",
          f"{config.Config.dst_image_path}{self.story.filename}_quote.jpeg",
          f"{config.Config.dst_image_path}{self.story.filename}_body.jpeg",
          f"{config.Config.dst_image_path}prelast_page.jpeg",
          f"{config.Config.dst_image_path}last_page.jpeg",
        ],
        # "Test caption for photo with #hashtags and mention users such @example",
        self.story.title + "\n" + tags
    )
    print(media)