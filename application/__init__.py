from flask import Flask


def create_app():
    """Construct the core app object"""
    app = Flask(__name__, instance_relative_config=False)

    # Config
    app.config.from_object('config.Config')

    with app.app_context():
        # Include Routes
        from .main import main_views
        app.register_blueprint(main_views.main_bp)

    return app
