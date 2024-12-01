

DOCPATH = "C:/Users/Valued Customer/Downloads/Will To Life.md"


class Story:
  def __init__(self) -> None:
    self.title = None
    self.subtitle = None
    self.image = None
    self.quote = None
    self.quoteauthor = None
    self.body = None
    self.footnote = None

  @property
  def filename(self):
    return self.title.lower().replace(" ", "_")

  def is_validate(self):
    if not (self.title and self.subtitle and self.quote and self.quoteauthor and self.body and self.footnote):
      return False
    return True
  
  def __str__(self) -> str:
    return f"Title: {self.title}\nSubtitle: {self.subtitle}\nQuote: {self.quote}\nAuthor: {self.quoteauthor}\nBody: {self.body}\nNote: {self.footnote}"


class Reader:
  def get_story(self, title):
    res = None

    with open(DOCPATH, "r", encoding="utf-8") as doc:
      content = doc.read().split("\n")
      for i, line in enumerate(content):
        if not line.startswith("##"):
          continue
        if not line[3:] == title:
          continue

        res = Story()
        res.title = title
        res.subtitle = content[i + 2]
        res.quote = content[i + 4]
        res.quoteauthor = content[i + 5]
        res.body = content[i + 7]
        res.footnote = content[i + 9]
        
        break

    if not res:
      raise Exception("No story found!")
    
    if not res.is_validate():
      print(res)
      raise Exception("Story is invalid!")

    return res
  

# def publish(title):
#   story = _get_story(title)
#   print(story)
#   return story


if __name__ == "__main__":
# publish("Inanity as Cause of Alcoholism")
  pass