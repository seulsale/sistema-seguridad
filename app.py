from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import requests
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '93jfaljef9ñ{a'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
DEVICE_ACCESS_TOKEN = 'a53bb6163a6680eebfcc6c8aec76d011bec713c6'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('logged_in'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Usuario y contraseña inválidos'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/api/motion')
def sensors():
    res = requests.get('http://10.0.0.3:8080/sensors.json?sense=motion_active')
    res = res.json()
    if len(res['motion_active']['data']) > 1:
        print('MOVIMIENTO')
        requests.post(f'https://api.particle.io/v1/devices/34002a000f47363336383437/trigger?access_token={DEVICE_ACCESS_TOKEN}', {
            'params': 'on'
        })
    return res

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
