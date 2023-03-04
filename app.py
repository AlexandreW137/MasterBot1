from flask import Flask, redirect, render_template
from requests import request
import requests
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')   
CLIENT_ID = config('CLIENT_ID')
REDIRECT_URL = config('REDIRECT_URL')
AUTH_URL = f"https://id.twitch.tv/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}&response_type=code&scope=user_subscriptions"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
API_URL = "https://api.twitch.tv/helix"

app = Flask(__name__, template_folder="arquivos/templates")

app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(AUTH_URL)

@app.route('/callback')
def callback():
    authorization_code = request.args.get('code')


    params = {
    'client_id': CLIENT_ID,
    'client_secret': SECRET_KEY,
    'code': authorization_code,
    'grant_type': 'authorization_code',
    'redirect_uri': REDIRECT_URL
}
    response = requests.post(TOKEN_URL, params=params)
    access_token = response.json().get('acess_token')
    print(access_token)


if __name__ == '__main__':
    app.run()