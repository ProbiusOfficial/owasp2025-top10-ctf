from flask import Flask
import os

app = Flask(__name__)

FLAG = open("/flag", "r").read().strip() if os.path.exists("/flag") else "flag{TEST_Dynamic_FLAG}"


@app.route("/flag")
def get_flag():
    return FLAG


@app.route("/")
def index():
    return "Flag Service - Access /flag to get the flag"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
