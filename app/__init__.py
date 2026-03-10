from flask import Flask
from .config import Config
from .extensions import db, migrate


def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so they're registered with SQLAlchemy
    from .models import user, product, cart, order, review  # noqa: F401

    # Register blueprints with flask-restx
    from .blueprints import register_blueprints
    register_blueprints(app)

    # Create tables if they don't exist (useful for dev)
    with app.app_context():
        db.create_all()

    return app
