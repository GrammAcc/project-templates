__all__ = [
    "create_app",
    "api",
    "db",
    "utils",
]

import json
import asyncio

from pathlib import Path

from flask import Flask
from flask_cors import CORS

from . import api, db, utils


__version__ = "0.0.1"


async def _create_app(custom_config: dict = {}, dev_mode: bool = True) -> Flask:
    """Flask application factory."""

    app = Flask(__name__, instance_relative_config=True)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    utils.set_dev_mode(dev_mode)

    if custom_config:
        app.config.from_mapping(custom_config)
    else:
        try:
            app.config.from_file("prod.json", load=json.load)
        except FileNotFoundError:
            print("No config file found.")
            print("Falling back to dev config...")
            print("DO NOT run this config in prod!")
            # Fallback config for dev environment.
            app.config.from_mapping(
                {
                    "SECRET_KEY": "dev",
                    "SEED_DB": True,
                    # "DB_URI": "postgresql+asyncpg://postgres:postgres@localhost:5432",
                    "DB_URI": f"sqlite+aiosqlite:///{app.instance_path}/packagename.db",
                    "PREFERRED_URL_SCHEME": "https",
                }
            )

    CORS(app)

    # Register routes for version 1 of the api.
    app.register_blueprint(api.v1.bp, url_prefix="/api/v1")

    # Setup the database.
    db.connect(app.config["DB_URI"], debug=utils.is_dev_mode())
    if app.config.get("SEED_DB", False):
        await db.seed()

    @app.teardown_appcontext
    async def cleanup_sqlalchemy_session(exception=None):
        await db.get_session_proxy().remove()

    return app


def create_app(custom_config: dict = {}, dev_mode: bool = True) -> Flask:
    return asyncio.run(_create_app(custom_config, dev_mode))
