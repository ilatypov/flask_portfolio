"""Desktop dev pages."""
from flask import Blueprint, render_template
from flask import current_app as app
#from import flask_portfolio.api import fetch_jobs


desktop_bp = Blueprint(
    'desktop_bp', __name__,
    template_folder='templates'
)

from . import routes
