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
    code = request.args.get('code')

    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URL
    }

    response = requests.post(TOKEN_URL, data=token_data).json()

    access_token = response['access_token']

    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }

    user_response = requests.get(f'{API_URL}/users', headers=headers).json()
    user_id = user_response['data'][0]['id']

    subs_response = requests.get(f'{API_URL}/subscriptions?broadcaster_id={user_id}', headers=headers).json()
    subs_list = [sub['user_name'] for sub in subs_response['data']]

    # realizar o sorteio
    ...

    return render_template('arquivos/app/templates/sorteio.html', subs_list=subs_list)

if __name__ == '__main__':
    app.run()