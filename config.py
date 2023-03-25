from os import getenv

class Config(object):
      API_HASH = getenv("API_HASH","d8e433e3b3e272aad4f1df2bdf24b8bd")
      API_ID = int(getenv("API_ID","25122159"))
      AS_COPY = True if getenv("AS_COPY", False) == "True" else False
      BOT_TOKEN = getenv("BOT_TOKEN", "6076403137:AAEIZHpc-aIs_dfob6Q7oqLNMUYK5i8yqIg")
      CHANNEL = list(x for x in getenv("CHANNEL_ID", "-1001640920080").replace("\n", " ").split(' '))
