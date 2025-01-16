from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import math
from PIL import Image
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key'

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL  -- Store hashed password as TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            number INTEGER NOT NULL,
            image BLOB NOT NULL,
            ascii_image TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def sieve_of_eratosthenes(n):
    primes = []
    is_prime = [True] * (n + 1)
    p = 2
    while (p * p <= n):
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)
    return primes

def plot_sieve(n):
    primes = set(sieve_of_eratosthenes(n))
    rows = int(math.ceil(math.sqrt(n)))
    cols = rows
    fig, ax = plt.subplots()
    square_size = 16
    
    for i in range(rows):
        for j in range(cols):
            number = i * cols + j + 1
            
            if number > n:
                break
            
            color = 'lightgreen' if number in primes else 'lightblue'
            
            rect = plt.Rectangle((j * square_size, (rows - 1 - i) * square_size), 
                                 square_size, square_size, edgecolor='black', facecolor=color)
            ax.add_patch(rect)
            
            ax.text(j * square_size + square_size / 2, (rows - 1 - i) * square_size + square_size / 2,
                    str(number), fontsize=12, ha='center', va='center')
    
    ax.set_xlim(0, cols * square_size)
    ax.set_ylim(0, rows * square_size)
    ax.set_aspect('equal')
    ax.axis('off')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode('utf-8')

def generate_ascii_image(image_data):
    img = Image.open(BytesIO(base64.b64decode(image_data)))
    img = img.convert('L')
    ascii_chars = '@%#*+=-:. '
    width, height = img.size
    aspect_ratio = height / width
    new_width = 100
    new_height = int(aspect_ratio * new_width * 0.55)
    img = img.resize((new_width, new_height))
    ascii_image = ''
    
    for i in range(new_height):
        for j in range(new_width):
            pixel_value = img.getpixel((j, i))
            ascii_image += ascii_chars[pixel_value // 32]
        ascii_image += '\n'

    return ascii_image.strip()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user = User(user_data[1], user_data[2])
            if user.check_password(password):
                session['username'] = user.email
                return redirect(url_for('menu'))
            else:
                return "Неправильный пароль. Попробуйте снова."
        else:
            return "Пользователь не найден. Пройдите регистрацию."

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if len(password) < 10:
            return "Пароль должен содержать не менее 10 символов."

        if password == confirm_password:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('menu'))
        else:
            return "Пароли не совпадают. Попробуйте еще раз."

    return render_template('register.html')

@app.route('/menu')
def menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html', username=session['username']) 

@app.route('/generate_sieve', methods=['GET', 'POST'])
def generate_sieve():
    if 'username' not in session:
        return redirect(url_for('login')) 
   
    image_data = None
    ascii_image_data = None

    if request.method == 'POST':
        user_input = int(request.form['number'])
        image_data = plot_sieve(user_input)
        ascii_image_data = generate_ascii_image(image_data)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (user_email, number, image, ascii_image) VALUES (?, ?, ?, ?)', 
                       (session['username'], user_input, image_data, ascii_image_data))
        conn.commit()
        conn.close()

    return render_template('generate_sieve.html', username=session['username'], image_data=image_data,
                           ascii_image=ascii_image_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT number, image, ascii_image FROM history WHERE user_email = ?', (session['username'],))
    history_records = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', username=session['username'], history=history_records)

if __name__ == "__main__":
    app.run(debug=True)