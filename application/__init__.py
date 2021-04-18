from flask import Flask
from flask_cors import CORS

def create_app():
    """Construct the core app object"""
    app = Flask(__name__, static_folder='../dist/static', instance_relative_config=False)

    # Config
    app.config.from_object('config.Config')

    from config import Config
    app.logger.info('>>> {}'.format(Config.FLASK_ENV))

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    with app.app_context():
        # Include Routes
        from .main import main_views
        app.register_blueprint(main_views.main_bp)

    return app
