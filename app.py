from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

OAUTH_PROVIDER_URL = 'http://localhost:5000/oauth'

@app.route('/api/protegida', methods=['GET'])
def protegida():
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not access_token:
        return jsonify({'error': 'Token de acesso não fornecido'})

    # Verificar o token de acesso com o provedor OAuth2
    response = requests.get(f'{OAUTH_PROVIDER_URL}/callback', params={'access_token': access_token})
    if response.status_code == 200:
        data = response.json()
        username = data.get('username')
        return jsonify({'message': f'Bem-vindo, {username}!'})

    return jsonify({'error': 'Token de acesso inválido'})

if __name__ == '__main__':
    app.run(port=5001)
