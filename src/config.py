from pathlib import Path
from decouple import Config

ROOT_DIR = Path(".").resolve()

config = Config(str(ROOT_DIR.joinpath(".env")))
MAX_MATCHES = config("MAX_MATCHES", default=2, cast=int)
MIN_MATCHES = config("MIN_MATCHES", default=1, cast=int)
MIN_PLAYERS = config("MIN_PLAYERS", default=2, cast=int)

DEBUG = config("DEBUG", default=False, cast=bool)
RANKS = ["IRON", "BRONZE", "SILVER"]
