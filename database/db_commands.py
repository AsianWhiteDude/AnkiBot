import asyncio
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select, insert, update, delete

from database.engine import sessionmaker


from database.user import User, Deck


async def add_set(user_id: int, set_name: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                statement=insert(Deck).values(deck_name=set_name,
                                              data={},
                                              user_id=user_id
                                            )
                                        )


async def add_card(user_id: int, key: str, value: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            record = await session.execute(
                statement=select(Deck).where(Deck.user_id == user_id)
            )
            record_instance = record.scalar()

            record_instance.data[key] = value

            await session.commit()


async def del_deck(user_id: int, set_name: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                statement=delete(Deck).where(Deck.user_id == user_id, Deck.deck_name == set_name)
            )


async def del_card(user_id: int, key: str, session_maker: sessionmaker) -> None:

    async with session_maker() as session:
        async with session.begin():
            # Find the deck belonging to the user
            record = await session.execute(
                select(Deck).where(Deck.user_id == user_id)
            )
            deck_instance = record.scalar()

            # Check if the deck exists and has data
            if deck_instance and key in deck_instance.data:
                # Delete the card by updating the JSONB data field
                updated_data = deck_instance.data.copy()
                del updated_data[key]

                # Update the deck with the modified data
                await session.execute(
                    update(Deck)
                    .where(Deck.user_id == user_id)
                    .values(data=updated_data)
                )

                # Commit the changes
                await session.commit()

async def get_decks(user_id: int, session_maker: sessionmaker) -> list:

    async with session_maker() as session:
        async with session.begin():
            # Find decks belonging to the user
            record = await session.execute(
                select(Deck.deck_name).where(Deck.user_id == user_id)
            )
            deck_names = [row for row in record.scalars().all()]

            return deck_names


async def get_cards(user_id: int, set_name: str, session_maker: sessionmaker) -> dict:
    async with session_maker() as session:
        async with session.begin():

            record = await session.execute(
                select(Deck.data).where(Deck.user_id == user_id, Deck.deck_name == set_name)
            )
            cards = {key: value for key, value in record.scalar().items()}
            return cards or {}

