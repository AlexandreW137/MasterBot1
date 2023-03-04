from flask import Flask, render_template
from requests import request
from decouple import config
import requests

app = Flask(__name__, template_folder="../templates")

@app.route('/')
def index():
    twitch_auth_url = f"https://id.twitch.tv/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}&response_type=code&scope=user_subscriptions"
    return f"<a href='{twitch_auth_url}'>Login com Twitch</a>"


@app.route('/sorteio')
def sorteio():
    return render_template('sorteio.html')
if __name__ == '__main__':
    app.run()
