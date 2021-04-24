from flask import Flask


def create_app(test_config=None):
    """Construct the core app object"""
    app = Flask(__name__, static_folder='../dist/static', instance_relative_config=False)

    # Config
    if test_config is None:
        app.config.from_object('config.Config')
        from flask_cors import CORS
        CORS(app, resources={r'/api/*': {'origins': '*'}})
    else:
        app.config.update(test_config)

    from config import Config
    app.logger.info('>>> {}'.format(Config.FLASK_ENV))

    with app.app_context():
        # Include Routes
        from .main import main_views
        app.register_blueprint(main_views.main_bp)

    return app
