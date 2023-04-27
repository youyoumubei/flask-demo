from flask import Flask
from api import bp as api_bp
from api2 import bp as api2_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api/v1')
app.register_blueprint(api2_bp, url_prefix='/api/v2')

if __name__ == '__main__':
    app.run(port=8999)
