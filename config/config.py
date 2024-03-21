import os
from dataclasses import dataclass
from environs import Env
from sqlalchemy.engine import URL

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

@dataclass
class Config:
    tg_bot: TgBot

@dataclass
class PostgreConfig:
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    POSTGRES_URL: URL


def load_database(path: str | None = None) -> PostgreConfig:
    env = Env()
    env.read_env(path)

    DB_HOST = str(env('DB_HOST'))
    DB_PORT = int(env('DB_PORT'))
    DB_USER = str(env('DB_USER'))
    DB_PASS = str(env('DB_PASS'))
    DB_NAME = str(env('DB_NAME'))
    POSTGRES_URL = URL.create(
        drivername="postgresql+asyncpg",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        database=DB_NAME,
        port=DB_PORT,
    )

    return PostgreConfig(DB_HOST=DB_HOST,
                         DB_PORT=DB_PORT,
                         DB_USER=DB_USER,
                         DB_PASS=DB_PASS,
                         DB_NAME=DB_NAME,
                         POSTGRES_URL=POSTGRES_URL
                         )


def load_config(path: str | None = None) -> Config:
    #creates config, take args from .env see example in .env.example


    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        )
    )