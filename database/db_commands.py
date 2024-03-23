from sqlalchemy import select, insert, delete
from database.engine import sessionmaker
from database.user import User, Deck, Card
from redis import Redis

async def add_set(user_id: int, set_name: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                statement=insert(Deck).values(deck_name=set_name,
                                              user_id=user_id
                                            )
                                        )

async def add_card(user_id: int, set_name: str, key: str, value: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            set_id = await session.execute(
                statement=select(Deck.deck_id).where(Deck.deck_name==set_name, Deck.user_id==user_id)
            )

            set_id = set_id.one_or_none()[0]

            await session.execute(
                statement=insert(Card).values(card_front=key, card_back=value, deck_id=set_id)
            )




async def del_deck(user_id: int, set_name: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            set_id = await session.execute(
                statement=select(Deck.deck_id).where(Deck.deck_name == set_name, Deck.deck_name == set_name)
            )

            set_id = set_id.one_or_none()[0]

            await session.execute(
                statement=delete(Card).where(Card.deck_id == set_id)
            )

            await session.execute(
                statement=delete(Deck).where(Deck.deck_id==set_id)
            )




async def del_card(user_id: int, set_name: str, key: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            set_id = await session.execute(
                statement=select(Deck.deck_id).where(Deck.deck_name == set_name, Deck.deck_name == set_name)
            )

            set_id = set_id.one_or_none()[0]

            await session.execute(
                statement=delete(Card).where(Card.deck_id==set_id, Card.card_front==key)
            )


async def get_decks(user_id: int, session_maker: sessionmaker) -> list:

    async with session_maker() as session:
        async with session.begin():
            # Find decks belonging to the user
            records = await session.execute(
                select(Deck.deck_name).where(Deck.user_id == user_id)
            )
            deck_names = records.scalars().all()
            return deck_names


async def get_cards(user_id: int, set_name: str, session_maker: sessionmaker) -> dict:
    async with session_maker() as session:
        async with session.begin():
            set_id = await session.execute(
                statement=select(Deck.deck_id).where(Deck.deck_name == set_name, Deck.user_id==user_id)
            )

            set_id = set_id.one_or_none()[0]
            keys = await session.execute(
                statement=select(Card.card_front).where(Card.deck_id==set_id)
            )
            values = await session.execute(
                statement=select(Card.card_back).where(Card.deck_id==set_id)
            )
            keys = keys.scalars().all()
            values = values.scalars().all()
            if not keys:
                return {}

            data = {keys[i]: values[i] for i in range(len(keys))}

            return data


async def create_user(user_id: int, username: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username
            )
            session.add(user)


async def is_user_exists(user_id: int, session_maker: sessionmaker, redis: Redis) -> bool:
    res = await redis.get(name='is_user_exists:' + str(user_id))
    if not res:
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(
                    statement=select(User).where(User.user_id == user_id)
                )
                sql_res = sql_res.scalars().all()

                await redis.set(name='is_user_exists:' + str(user_id), value=1 if sql_res else 0)
                return bool(sql_res)
    else:
        return bool(res)
