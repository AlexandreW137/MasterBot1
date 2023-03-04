from flask import Flask, render_template
from requests import request
import requests

app = Flask(__name__, template_folder="../templates")

@app.route('/')
def index():
    return f"<a href=''>Login com Twitch</a>"


@app.route('/sorteio')
def sorteio():
    return render_template('arquivos/app/templates/sorteio.html')
if __name__ == '__main__':
    app.run()
