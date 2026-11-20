from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 5001))
    app.run(host="127.0.0.1", port=port)
