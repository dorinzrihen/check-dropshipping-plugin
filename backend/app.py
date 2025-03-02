from flask import Flask
from flask_cors import CORS
from routes.upload import upload_bp
from routes.search import search_bp

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
CORS(app)

# Register blueprints (modular routing)
app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(search_bp, url_prefix="/search")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
