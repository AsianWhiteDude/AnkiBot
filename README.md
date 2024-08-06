## Project Overview
Development of an asynchronous Telegram bot that facilitates the memorization process using electronic flashcards (Anki). Users can create their own decks of cards, study them, and track their progress. Technologies used: Python, Aiogram, PostgreSQL, Redis, Telegram Bot API.


- Implemented the project in Python using the Aiogram library.
- Implemented asynchronous user registration.
- Used PostgreSQL as the database.
- Utilized Redis for caching to reduce database load, thus improving performance and reducing the bot's response time.
- Also employed an FSM model based on Redis, which allows for efficient management of the bot's states and processing of various events.
