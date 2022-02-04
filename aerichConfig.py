import toml

# import os

config = toml.load("config.toml")

# DB init
DATABASE_URL = f"postgres://{config['postgres']['username']}:{config['postgres']['password']}\
@{config['postgres']['server']}:{config['postgres']['port']}/{config['postgres']['db_name']}"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
