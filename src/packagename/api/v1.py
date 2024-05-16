"""This module provides the RESTful api entry_points for v1 of the backend."""

from __future__ import annotations

__all__ = [
    "replace_me",
    "coffee",
]

from flask import Blueprint, jsonify, request, Response
from sqlalchemy import select

from packagename import db


VALID_QUERY_PARAMS = ["q"]
"""A list including all GET parameters accepted by the API.

This is useful for a simple first-pass validation of
parameters in the middleware layer. Individual endpoints may
perform validation of query params specific to them.
"""


bp = Blueprint("v1", __name__)
"""This blueprint contains all routes for version 1 of the api."""


@bp.after_request
async def _add_caching_headers(res: Response) -> Response:
    """Set caching response headers.

    API resources are typically updated daily at most often, so
    we tell clients to cache responses for 24 hours. This does
    not affect static or templated pages. Only JSON responses from
    the API.
    """

    res.headers["Cache-Control"] = "max-age=86400"
    return res


@bp.before_request
async def _invalid_query_response() -> Response | None:
    """Ensure that there are no invalid query parameters before passing the request
    to the view function.

    The flask @Blueprint.before_request hook causes request processing to stop if a
    value other than None is returned, so this hook should prevent processing of
    malformed GET requests on all routes.
    """

    invalid_params = [i for i in request.args if i not in VALID_QUERY_PARAMS]
    if invalid_params:
        res = jsonify(
            {
                "object": "error",
                "status": 400,
                "details": "Invalid query parameters.",
                "invalid_parameters": invalid_params,
            }
        )
        res.status_code = 400
        res.content_type = "application/problem+json"
        return res
    else:
        return None


@bp.route("/replace-me", methods=["GET"])
async def replace_me() -> Response:
    """Endpoint that returns all `example` resources.

    The results can be filtered by their `name` property with the `q`
    query param.

    HTTP Errors:
        400 Bad Request:
            If passed invalid query parameters.
    """

    async with db.get_session() as session:
        records = (
            await session.execute(
                select(db.models.Example).where(
                    db.models.Example.name == request.args["q"]
                )
            )
            if "q" in request.args
            else await session.execute(select(db.models.Example))
        )
        response = jsonify(db.models.results_as_resources(records.scalars().all()))
        return response


@bp.route("/coffee", methods=["GET"])
def coffee() -> Response:
    """Endpoint that returns a status 418 response for compliance
    with the HTCPCP protocol as defined in RFC 2324."""

    res = jsonify(
        {
            "object": "error",
            "status": 418,
            "details": "The packagename.com coffee pot was replaced with a tea kettle. \
This endpoint is maintained for compliance with the HTCPCP/1.0 standard as defined in \
RFC 2324.",
            "see_also": "https://www.rfc-editor.org/rfc/rfc2324",
        }
    )
    res.status_code = 418
    res.content_type = "application/problem+json"
    return res
