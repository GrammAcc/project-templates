"""The SQLAlchemy ORM schema."""

from __future__ import annotations

__all__ = [
    "BaseModel",
    "Example",
    "MTMExample",
    "OTMExample",
    "results_as_resources",
    "get_resource_names",
]

import functools

from typing import Protocol, Any, Sequence

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
)
from sqlalchemy.ext.asyncio import AsyncAttrs

from packagename.utils import snake_to_hyphen, get_domain

_INTERNAL_FIELDS: set[str] = {"id"}


class ResourceModel(Protocol):
    """SQLAlchemy models that correspond to API resources should
    have these methods implemented."""

    def as_dict(self) -> dict[str, Any]: ...

    def to_resource(self) -> dict[str, Any]: ...

    def get_uri(self) -> str: ...


class BaseModel(AsyncAttrs, DeclarativeBase):
    def __repr__(self) -> str:  # pragma: no cover
        columns = ", ".join([f"{col}={val}" for col, val in self.as_dict().items()])
        return f"{self.__class__.__name__}({columns})"

    def as_dict(self) -> dict[str, Any]:  # pragma: no cover
        """Convert this model to a dict of its column names and values."""

        new_dict = {col.key: getattr(self, col.key) for col in self.__table__.columns}
        return new_dict

    def get_relations(self) -> dict[str, Any]:
        """Abstract method to get a dict of the Model's related resources."""

        raise NotImplementedError

    def to_resource(self, include_relations=True) -> dict[str, Any]:  # pragma: no cover
        """Convert this model to a dict representing its public API resource and
        return the result.

        Args:
            include_relations:
                If True, include any related resources in the built dict.
                If False, do not include any related resources.
                Use False when adding this resource as a related resource to another
                resource to avoid an infinite loop.
        Returns:
            dict:
                The constructed resource representation of this model's data excluding
                any internal or sensitive fields.
        """

        res_dict = {
            k: v for k, v in self.as_dict().items() if k not in _INTERNAL_FIELDS
        }
        res_dict["uri"] = self.get_uri()
        if include_relations:
            res_dict.update(self.get_relations())
        return res_dict

    def get_uri(self) -> str:  # pragma: no cover
        """Return the direct URI for the resource record that this Model instance
        corresponds to."""

        return f"{get_domain()}/api/v1/\
{snake_to_hyphen(self.__tablename__)}/{self.id}"  # type: ignore[attr-defined]


table_example_mtmexample = Table(
    "example_mtmexample",
    BaseModel.metadata,
    Column("example_id", ForeignKey("example.id"), primary_key=True),
    Column("mtmexample_id", ForeignKey("mtmexample.id"), primary_key=True),
)


class Example(BaseModel):
    """An example ORM model."""

    __tablename__ = "example"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    mtmexamples: Mapped[list["MTMExample"]] = relationship(
        secondary=table_example_mtmexample,
        back_populates="examples",
        lazy="selectin",
    )
    otmexamples: Mapped[list["OTMExample"]] = relationship(
        back_populates="example", lazy="selectin"
    )

    def get_relations(self) -> dict[str, Any]:
        """Return a dictionary of this model's related resources."""

        return {
            "mtmexamples": [
                r.to_resource(include_relations=False) for r in self.mtmexamples
            ],
            "otmexamples": [
                r.to_resource(include_relations=False) for r in self.otmexamples
            ],
        }


class MTMExample(BaseModel):
    """An example ORM model for many-to-many relations."""

    __tablename__ = "mtmexample"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    examples: Mapped[list["Example"]] = relationship(
        secondary=table_example_mtmexample,
        back_populates="mtmexamples",
        lazy="selectin",
    )

    def get_relations(self) -> dict[str, Any]:
        """Return a dictionary of this model's related resources."""

        return {
            "examples": [r.to_resource(include_relations=False) for r in self.examples],
        }


class OTMExample(BaseModel):
    """An example ORM model for one-to-many relations."""

    __tablename__ = "otmexample"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    example_id: Mapped[int] = mapped_column(ForeignKey("example.id"))
    example: Mapped["Example"] = relationship(
        back_populates="otmexamples", lazy="selectin"
    )

    def get_relations(self) -> dict[str, Any]:
        """Return a dictionary of this model's related resources."""

        return {"example": self.example.to_resource(include_relations=False)}


def results_as_resources(
    select_results: Sequence[ResourceModel],
) -> list[dict[str, Any]]:
    """Convert a scalar result set from a list of Model instances to a list of their
    JSON-serializable resource representations."""

    return [record.to_resource() for record in select_results]


_RESOURCES = [
    Example,
    MTMExample,
    OTMExample,
]


@functools.cache
def get_resource_names() -> list[str]:
    """Get a list of names of all public resources provided by the API."""

    return [i.__tablename__ for i in _RESOURCES]
