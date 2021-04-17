from os import environ as _environ

from server.set_env import setup_env as _setup_env

_setup_env()


IS_PROD = _environ.get("IS_DEV") is None

if IS_PROD:
    print(
        "assuming production environment, change `IS_DEV` in your .env.json to switch to dev"
    )

DATABASE_URL = _environ["DATABASE_URL"].replace("postgres://", "postgresql://", 1)
ACCESS_KEY = _environ["ACCESS_KEY"]

del _environ
