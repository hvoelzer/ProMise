

from flask import Flask, request
from flask_cors import CORS
from control import Control


control = Control()
app = Flask(__name__)
CORS(app)
# Members API Route


@app.route("/")
def home():
    return "Home"


@app.route("/import_raw_data", methods=['POST'])
def import_raw_data():
    file = request.get_json()
    control.loadRawfile(file)

    print("done")

    return "Done", 201

@app.route("/get_graph", methods=['GET'])
def get_graph():
    return control.getEdgesAsJson()


if __name__ == "__main__":
    app.run(debug=True)
