from flask import Flask, request

app = Flask(__name__)

#Members API Route
@app.route("/")
def home():
    return "Home"

@app.route("/import_raw_data", methods=['POST'])
def import_raw_data():
    file = request.get_json()
    print(file)
    return "Done", 201

if __name__ == "__main__":
    app.run(debug=True)