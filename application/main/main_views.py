from flask import Blueprint, jsonify, make_response
from math import log, sqrt, exp
from scipy import stats

main_bp = Blueprint('main_bp', __name__,
                    url_prefix='',
                    )


@main_bp.route('/')
def index_client():
    """Landing page / Home page"""

    return jsonify({
        "message": "Find the api docs at api.getgreeks.com/apidocs",
        "gif": "http://gph.is/2qECeML"
    })


@main_bp.route('/ping/')
def ping():
    """Testing route ping...pong"""
    return jsonify('pong!')
