import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes import register_routes

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = 'macuin_super_secreto'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    if not app.config['DEBUG']:
        app.config['TEMPLATES_AUTO_RELOAD'] = False 
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000 
    
    CORS(app)
    
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])