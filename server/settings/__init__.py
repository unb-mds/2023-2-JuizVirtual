from pathlib import Path

from environ import Env

BASE_DIR = Path(__file__).parent.parent.parent

# Load environment variables from config/.env file. See
# https://django-environ.readthedocs.io/en/latest/

env = Env()
READ_DOTENV = env.bool("DJANGO_READ_DOTENV", default=False)

if READ_DOTENV:
    env.read_env(BASE_DIR / "config" / ".env")
