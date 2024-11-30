# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import os
from functools import wraps
from connectDB import funcMongoDB

app = Flask(__name__)
# Generate a secure random secret key
app.secret_key = os.urandom(24)



def hash_password(password):
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', 
                                   password.encode('utf-8'), 
                                   salt, 
                                   100000)
    return {'salt': salt,'hash': pwd_hash}

# Password verification
def verify_password(stored_password, provided_password):
    try:
        # If stored_password is already a string, hash the provided password
        if isinstance(stored_password, str):
            # Simple compatibility method for existing passwords
            return stored_password == provided_password
        # If stored as a hashed dictionary
        salt = stored_password.get('salt', b'')
        stored_hash = stored_password.get('hash', b'')
        
        # Hash the provided password with the same salt
        pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        
        return pwd_hash == stored_hash
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def add_cache_control_header(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

# Routes
@app.route('/')
@login_required
def index():
    db = funcMongoDB(index_='name')
    db.connect_mongodb()
    users = db.get_data()
    db.stopClient()
    return render_template('index.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = funcMongoDB(index_='user')
        user = db.loginUser(username)
        print(user)
        if user and verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['user']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        db = funcMongoDB()
        db.connect_mongodb()
        data = {'name':name,'email':email,'age':age}
        result = db.addNewData(data)
        message = 'User profile added successfully! id: ' + str(result)
        flash(message, 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    db = funcMongoDB()
    db.connect_mongodb()
    user = db.findOne(user_id)
    if not user:
        db.stopClient()
        flash('User not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        data = {'_id':user_id,'name':name,'email':email,'age':age}
        db.update(data)
        flash('User profile updated successfully', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', user=user)

@app.route('/delete/<user_id>')
@login_required
def delete_user(user_id):
    db = funcMongoDB()
    db.connect_mongodb()
    db.delete(user_id)
    db.stopClient()
    flash('User profile deleted successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)  # Set to False in production