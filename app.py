from flask import Flask, request, render_template
from threading import Thread

app = Flask(__name__)


@app.route("/check")
def hello_world():
    return "Hello world"

def run():
  app.run(host='0.0.0.0', port=80)

def keep_alive():
  t = Thread(target=run)
  t.start()
