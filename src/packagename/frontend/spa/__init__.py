"""This subpackage contains routes for the single-page app frontend."""

from __future__ import annotations

__all__ = ["bp"]


from flask import Blueprint, send_from_directory
from werkzeug.exceptions import NotFound


bp = Blueprint("static_frontend", __name__, template_folder="site")
"""This blueprint contains all routes for the built HTML/CSS/JS."""


@bp.route("/", methods=["GET"])
def serve_spa():
    return send_from_directory("frontend/spa/site", "index.html")


@bp.route("/<path:path>", methods=["GET"])
def serve_spa_resources(path):
    try:
        return send_from_directory("frontend/spa/site", path)
    except NotFound:
        return send_from_directory("frontend/spa/site", "index.html")
