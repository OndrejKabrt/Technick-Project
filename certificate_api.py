from flask import Flask
from Clases.Certificate.certificate_routes import create_certificate_routes

app = Flask(__name__)
create_certificate_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)