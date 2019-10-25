from flask import Flask

app = Flask("Telefonbuch")

@app.route("/")
@app.route("/index")
def index():
    return "test"

if __name__ == "__main__":
    app.run(debug=True, port=5000)