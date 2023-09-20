from os.path import join
from pathlib import Path

from environ import Env

BASE_DIR = Path(__file__).parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

# Load environment variables from config/.env file. See
# https://django-environ.readthedocs.io/en/latest/

env = Env()
env.read_env(join(BASE_DIR, "config", ".env"))
