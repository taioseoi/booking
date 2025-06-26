from flask import Flask
from routes.auth import auth_bp
from routes.booking import booking_bp
from routes.linebot import linebot_bp
from routes.payments import payment_bp
from routes.upload_slip_ai import ai_upload_bp
from config import SECRET_KEY
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(linebot_bp, url_prefix='/linebot')
    app.register_blueprint(payment_bp, url_prefix='/payment')
    app.register_blueprint(ai_upload_bp, url_prefix='/ai_upload')
    app.register_blueprint(admin_bp)
    for rule in app.url_map.iter_rules():
        print(rule)

    @app.route('/')
    def hello():
        return "Hello from Render!"

    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)