from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__, template_folder='templates/vue_template')


@main_bp.route('/')
def index():
    """Landing page / Home page"""
    return jsonify('pong!')


@main_bp.route('/ping')
def ping():
    """Testing route ping...pong"""
    return jsonify('pong!')

@main_bp.route('/about')
def about():
    """About page"""
    print("about")
