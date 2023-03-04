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
print(CLIENT_ID)
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
    
    return render_template('subscribers.html', authorization_code=authorization_code)


if __name__ == '__main__':
    app.run()