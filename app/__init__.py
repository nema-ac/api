from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configure app here (e.g., app.config.from_object('config.Config'))

    # Register blueprints or routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
