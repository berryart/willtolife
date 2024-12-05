from content_io import IO
import config


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

  @property
  def script(self):
    return f"# {self.title}\n\n{self.subtitle}\n\n{self.quote}\n{self.quoteauthor}\n\n{self.body}\n\n{self.footnote}"

  def is_validate(self):
    if not (self.title and self.subtitle and self.quote and self.quoteauthor and self.body and self.footnote):
      return False
    return True
  
  def __str__(self) -> str:
    return f"Title: {self.title}\nSubtitle: {self.subtitle}\nQuote: {self.quote}\nAuthor: {self.quoteauthor}\nBody: {self.body}\nNote: {self.footnote}"
  

class Reader:
  def __init__(self, title):
    self.title = title

  def makescript(self):
    res = None

    with open(config.Config.script_path, "r", encoding="utf-8") as doc:
      content = doc.read().split("\n")
      for i, line in enumerate(content):
        if not line.startswith("##"):
          continue
        if not line[3:] == self.title:
          continue

        res = Story()
        res.title = self.title
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
    
    io = IO(self.title)
    with open(io.script, "w") as f:
      f.write(res.script)
      print(f"Script saved: {io.script}")

    return res
  
  def readscript(self):
    io = IO(self.title)
    with open(io.script, "r") as f:
      text = f.read().split("\n")
      res = Story()
      res.title = self.title
      res.subtitle = text[2]
      res.quote = text[4]
      res.quoteauthor = text[5]
      res.body = text[7]
      res.footnote = text[9]
    return res
