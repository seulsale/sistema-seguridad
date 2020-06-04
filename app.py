from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = '93jfaljef9ñ{a'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
DEVICE_ID='34002a000f47363336383437'
DEVICE_ACCESS_TOKEN = 'a53bb6163a6680eebfcc6c8aec76d011bec713c6'
CAMERA_IP=os.environ['CAMERA_IP']

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
    content = {
        'camera_ip': CAMERA_IP
    }
    return render_template('index.html', content=content)

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

@app.route('/stats')
def stats():
    content = {
        'camera_ip': CAMERA_IP
    }
    return render_template('stats.html', content=content)
    
@app.route('/api/motion')
def sensors():
    res = requests.get(f'{CAMERA_IP}/sensors.json?sense=motion_active')
    res = res.json()
    movement = 0
    if len(res['motion_active']['data']) > 1:
        print('MOVIMIENTO')
        requests.post(f'https://api.particle.io/v1/devices/{DEVICE_ID}/trigger?access_token={DEVICE_ACCESS_TOKEN}', {
            'params': 'on'
        })
        movement = 1
    return jsonify(
        movement=movement
    )



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
