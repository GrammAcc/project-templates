"""Seed a local database without running the application."""

if __name__ != "__main__":
    raise ImportError("Standalone script cannot be imported!")

import asyncio

from packagename import db

db.connect("sqlite+aiosqlite:///local.db")

asyncio.run(db.seed())
