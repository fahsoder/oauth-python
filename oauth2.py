from flask import Flask, redirect, jsonify, request, abort
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['ALGORITHM'] = 'HS256'

# Dados simulados do usuário
USERS = {
    'user1': {
        'username': 'user1',
        'password': 'password1',
    },
    'user2': {
        'username': 'user2',
        'password': 'password2',
    }
}

@app.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    # Validação do usuário e senha
    username = request.form.get('username')
    password = request.form.get('password')
    if username in USERS and USERS[username]['password'] == password:
        # Gerar token de acesso com data de expiração de 1 hora
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], app.config['ALGORITHM'])
        if request.method == 'POST':
            return jsonify({'access_token': ('Bearer ' + token)})
        return redirect('/oauth/callback?access_token=' + token)
    else:
        abort(400, jsonify({'error': 'Credenciais inválidas'}))

@app.route('/oauth/callback')
def callback():
    # Obter o token de acesso
    token = request.args.get('access_token')
    if token:
        try:
            # Verificar e decodificar o token de acesso
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['ALGORITHM']])
            username = payload['username']
            if not username in USERS:
                raise jwt.InvalidTokenError
            return jsonify({'username': username})
        except jwt.ExpiredSignatureError:
            abort(400, jsonify({'error': 'Token expirado'}))
        except jwt.InvalidTokenError:
            abort(400, jsonify({'error': 'Token inválido'}))
    else:
        return jsonify({'error': 'Token de acesso não fornecido'})

if __name__ == '__main__':
    app.run()
