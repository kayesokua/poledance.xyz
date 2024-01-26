from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from app.extensions.db import db, migrate


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    csrf = CSRFProtect(app)
    db.init_app(app)
    bootstrap = Bootstrap(app)

    with app.app_context():
        from app.models import User
        db.create_all()
        migrate.init_app(app, db, compare_type=True)
    
    from app.accounts.routes import bp as accounts
    app.register_blueprint(accounts)
    
    app.add_url_rule("/login", endpoint='accounts.index')
    app.add_url_rule("/register", endpoint='accounts.register')
    
    @app.route("/")
    def index():
        return render_template("/index.html", title="Cover")

    return app