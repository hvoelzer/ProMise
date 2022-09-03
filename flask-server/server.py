

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


@app.route("/get_history_graph", methods=['GET'])
def get_history_graph():
    return control.getEdgesAsJsonHistory()


@app.route("/filter", methods=['POST'])
def filter():
    filter = request.get_json()
    control.applyFilter(filter)

    print("done")

    return "Done", 201


@app.route("/get_event_log", methods=['GET'])
def get_event_log():
    return control.getEventLog()


@app.route("/change_selected_node", methods=['POST'])
def change_selected_node():
    id = request.get_json()
    control.changeLastNode(id)

    print("done")

    return "Done", 201


if __name__ == "__main__":
    app.run(debug=True)
