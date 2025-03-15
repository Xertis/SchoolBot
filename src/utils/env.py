import os
from dotenv import load_dotenv

load_dotenv()


class Constants:
    pass


for key, val in os.environ.items():
    setattr(Constants, key, val)
