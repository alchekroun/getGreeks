from flask import Flask


def create_app(test_config=None):
    """Construct the core app object"""
    app = Flask(__name__, instance_relative_config=False)

    # Config
    if test_config is None:
        app.config.from_object('config.Config')
        from flask_cors import CORS
        CORS(app, resources={r'/*': {'origins': '*'}}, support_credentials=True)
    else:
        app.config.update(test_config)

    from config import Config
    app.logger.info('>>> {}'.format(Config.FLASK_ENV))

    # Config flasgger
    from flasgger import Swagger
    app.config['SWAGGER'] = {
        'title': 'GetGreeks API',
        'hide_top_bar': True,
        'version': '0.2.0',
        'doc_expansion': "list",
        'uiversion': 3
    }
    Swagger(app)

    with app.app_context():
        # Include Routes
        from .main import main_views
        from .calc import calc_views
        app.register_blueprint(main_views.main_bp)
        app.register_blueprint(calc_views.calc_bp)

    return app
