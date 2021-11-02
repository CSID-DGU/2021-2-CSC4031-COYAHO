from flask import Flask, request
from api import namespace

app = Flask(__name__)
app.register_blueprint(namespace.namespace_api, url_prefix='/namespaces')

if __name__ == '__main__':
    app.run(debug=True)