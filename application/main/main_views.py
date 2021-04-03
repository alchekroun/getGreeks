from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    """Landing page / Home page"""
    print("ok")

@main_bp.route('/about')
def about():
    """About page"""
    print("about")
