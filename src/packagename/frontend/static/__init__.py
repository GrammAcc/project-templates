"""This subpackage contains routes for the static frontend."""

from __future__ import annotations

__all__ = ["bp"]


from flask import Blueprint, send_from_directory
from werkzeug.exceptions import NotFound


bp = Blueprint("static_frontend", __name__)
"""This blueprint contains all routes for the static HTML/CSS/JS."""


@bp.route("/", defaults={"path": ""}, methods=["GET"])
@bp.route("/<path:path>", methods=["GET"])
def serve_static_site(path):
    if path == "":
        return send_from_directory("frontend/static/site", "index.html")
    try:
        return send_from_directory("frontend/static/site", path)
    except NotFound:
        return send_from_directory("frontend/static/site", path + ".html")
