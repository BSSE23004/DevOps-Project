from flask import Flask, jsonify
import os

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "v1")

@app.route("/")
def index():
    return jsonify({"service": "simple-api", "version": VERSION})

@app.route("/healthz")
def health():
    return "OK", 200

@app.route("/version")
def version():
    return VERSION
