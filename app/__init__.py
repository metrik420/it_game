from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app
