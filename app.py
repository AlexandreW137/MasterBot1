from flask import Flask, redirect, render_template
from flask import request
from decouple import config
import requests
def get_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': CLIENT_ID
    }
    response = requests.get(f'{API_URL}/users', headers=headers)
    data = response.json()  
    user_info = {
        'id': data['data'][0]['id'],  # adiciona o ID do usuário ao dicionário
        'name': data['data'][0]['display_name'],
        'image_url': data['data'][0]['profile_image_url']
    }
    return user_info

def get_subscribers(access_token, broadcaster_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': CLIENT_ID
    }
    response = requests.get(f'{API_URL}/subscriptions?broadcaster_id={broadcaster_id}', headers=headers)
    data = response.json()
    subscribers = [subscriber['user_name'] for subscriber in data['data']]
    return subscribers



def get_followers(access_token, channel_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': CLIENT_ID
    }
    response = requests.get(f'{API_URL}/users/follows?to_id={channel_id}', headers=headers)
    data = response.json()
    followers = [follower['from_name'] for follower in data['data']]
    return followers

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
def redirecionamento():
    CODE = request.args.get('code')
    params = {
    'client_id': CLIENT_ID,
    'client_secret': SECRET_KEY,
    'code': CODE,
    'grant_type': 'authorization_code',
    'redirect_uri': REDIRECT_URL
}
    response = requests.post(TOKEN_URL, params=params)
    ACCESS_TOKEN = response.json().get('access_token')

    # obtém o nome do usuário usando a função 'get_user_name'
    user_info = get_user_info(ACCESS_TOKEN)
    
    followers = get_followers(ACCESS_TOKEN, user_info['id'])

   

    return render_template('sorteio.html', user_info=user_info,followers=followers)



if __name__ == '__main__':
    app.run(debug=True)