from pathlib import Path

import pytest

from packagename import create_app, db


@pytest.fixture
def fixt_api_resources():
    """A list of the names of resources available on the API."""

    return db.models.get_resource_names()


@pytest.fixture
def fixt_app():
    """The flask application in dev mode."""

    testing_config = {
        "DB_URI": "sqlite+aiosqlite:///:memory:",
        "SEED_DB": True,
        "SECRET_KEY": "dev",
        "PREFERRED_URL_SCHEME": "https",
    }

    app = create_app(custom_config=testing_config, dev_mode=True)

    yield app


@pytest.fixture
def fixt_client(fixt_app):
    """The client used to make requests to the application under test."""

    return fixt_app.test_client()


@pytest.fixture
def fixt_prod_app():
    """The flask application in dev mode with production-equivalent data."""

    db_path = Path("tests/prod_data.db").absolute()

    if not db_path.exists():
        raise Exception(
            "Production-equivalent database not found. \
Copy the production database to 'tests/prod_data.db' before running the testsuite."
        )

    testing_config = {
        "DB_URI": "".join(["sqlite+aiosqlite:///", str(db_path)]),
        "SEED_DB": False,
        "SECRET_KEY": "dev",
        "PREFERRED_URL_SCHEME": "https",
    }

    app = create_app(custom_config=testing_config, dev_mode=True)

    yield app


@pytest.fixture
def fixt_prod_client(fixt_prod_app):
    """The client used to make requests to the application under test using
    production-equivalent data."""

    return fixt_prod_app.test_client()


@pytest.fixture
def fixt_runner(fixt_app):
    """The CLI test runner for the flask application."""

    return fixt_app.test_cli_runner()
