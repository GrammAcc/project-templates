"""Helper functions."""

__all__ = [
    "hyphen_to_snake",
    "snake_to_hyphen",
    "set_dev_mode",
    "is_dev_mode",
    "get_domain",
]


def hyphen_to_snake(hyphenated: str) -> str:  # pragma: no cover
    """Return `hyphenated` with all hyphen characters replaced by underscores.

    Useful for converting url params to corresponding python identifiers.
    """

    return hyphenated.replace("-", "_")


def snake_to_hyphen(snaked: str) -> str:  # pragma: no cover
    """Return `snaked` with all underscore characters replaced by hyphens.

    Useful for converting python identifiers to url params.
    """

    return snaked.replace("_", "-")


_DEV_MODE: bool = True


def set_dev_mode(dev_mode: bool) -> None:
    """Public setter for the _DEV_MODE constant."""

    global _DEV_MODE
    _DEV_MODE = dev_mode


def is_dev_mode() -> bool:
    """Are we in a dev environment? False means prod."""
    return _DEV_MODE


def get_domain() -> str:
    """Return the full domain name and schema identifier for the api without
    a flask application context.

    Useful for constructing URIs for specific resources in the db.
    """

    if is_dev_mode():
        return "http://api.packagename.local"
    else:
        return "https://www.packagename.com"  # pragma: no cover
