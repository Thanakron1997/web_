# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import os
from functools import wraps
from connectDB import funcMongoDB
from datetime import datetime, time
app = Flask(__name__)
import func.function as fc

# Generate a secure random secret key
app.secret_key = os.urandom(24)

# Generate a secure random secret key
@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)

def updateNextVist(users):
    users = [{
            **i,
            'nextVisit': (nextVisit['next_visit'] if (nextVisit := fc.getNextVist(i['visit_data'])) else "NA")
            if 'visit_data' in i else "NA",
            'nextVisitDate': (nextVisit['next_visit_date'] if nextVisit else "NA")
            if 'visit_data' in i else "NA",
        }
        for i in users]
    return users

def updateNextVistUser(user):
    if len(user['visit_data']) > 0:
        nextVisit = fc.getNextVist(user['visit_data'])
        user['nextVisit'] =  nextVisit['next_visit']
        user['nextVisitDate'] =  nextVisit['next_visit_date']
        if 'lastVisit' in nextVisit.keys():
            user['lastVisit'] = True
    else:
        user['nextVisit'] =  "NA"
        user['nextVisitDate'] =  "NA"

    return user

def hash_password(password):
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
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
    return render_template('index.html')

@app.route('/project1')
@login_required
def project1():
    db = funcMongoDB(index_='name')
    db.connect_mongodb()
    users = db.get_data()
    db.stopClient()
    users = updateNextVist(users) 
    return render_template('project1.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = funcMongoDB(index_='user')
        user = db.loginUser(username)
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

@app.route('/<last_page>/add', methods=['GET', 'POST'])
@login_required
def add_user(last_page):
    if request.method == 'POST':
        project = request.form['project']
        subjectNumber = request.form['subjectNumber']
        randomizeNumber = request.form['randomizeNumber']
        group = request.form['group']
        groupStudy = request.form['groupStudy']
        ra = request.form['ra']
        rn = request.form['rn']
        status = request.form['status']
        name = request.form['name']
        hn = request.form['hn']
        dob = request.form['dob']
        phone = request.form['phone']
        address = request.form['address']
        parent = request.form['parent']
        visits = request.form.getlist('visit')
        visit_dates = request.form.getlist('visitdate')
        next_visits = request.form.getlist('nextvisit')
        next_visit_dates = request.form.getlist('nextvisitDate')
        visit_data= []
        for visit, visit_date, next_visit,next_visit_date in zip(visits, visit_dates, next_visits,next_visit_dates):
            visit_data.append({
                'visit': visit,
        'visit_date': datetime.combine(datetime.strptime(visit_date, '%Y-%m-%d').date(), time.min),  # Convert to datetime
        'next_visit': next_visit,
        'next_visit_date': datetime.combine(datetime.strptime(next_visit_date, '%Y-%m-%d').date(), time.min)  # Convert to datetime
            })
        db = funcMongoDB()
        db.connect_mongodb()
        data = {'project':project,'subjectNumber':subjectNumber,'randomizeNumber':randomizeNumber,'group':group,'groupStudy':groupStudy,'ra':ra,'rn':rn,'status':status,'name':name,'hn':hn,'dob':dob,'phone':phone,'address':address,'parent':parent,'visit_data':visit_data}
        result = db.addNewData(data)
        message = 'User profile added successfully! id: ' + str(result)
        flash(message, 'success')
        db.stopClient()
        return redirect(url_for(last_page))
    return render_template('add.html',last_page=last_page)

@app.route('/edit/<last_page>/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id,last_page):
    db = funcMongoDB()
    db.connect_mongodb()
    user = db.findOne(user_id)
    user = updateNextVistUser(user)
    if not user:
        db.stopClient()
        flash('User not found', 'error')
        return redirect(url_for(last_page))
    
    if request.method == 'POST':
        project = request.form['project']
        subjectNumber = request.form['subjectNumber']
        randomizeNumber = request.form['randomizeNumber']
        group = request.form['group']
        groupStudy = request.form['groupStudy']
        ra = request.form['ra']
        rn = request.form['rn']
        status = request.form['status']
        name = request.form['name']
        hn = request.form['hn']
        dob = request.form['dob']
        phone = request.form['phone']
        address = request.form['address']
        parent = request.form['parent']
        visits = request.form.getlist('visit')
        visit_dates = request.form.getlist('visitdate')
        next_visits = request.form.getlist('nextvisit')
        next_visit_dates = request.form.getlist('nextvisitDate')
        phoneCalls = request.form.getlist('PhoneCall')
        phoneCallDates = request.form.getlist('PhoneCallDate')
        visit_data= []
        for visit, visit_date, next_visit,next_visit_date in zip(visits, visit_dates, next_visits,next_visit_dates):
            visit_data.append({
                'visit': visit,
        'visit_date': datetime.combine(datetime.strptime(visit_date, '%Y-%m-%d').date(), time.min),  # Convert to datetime
        'next_visit': next_visit,
        'next_visit_date': datetime.combine(datetime.strptime(next_visit_date, '%Y-%m-%d').date(), time.min)  # Convert to datetime
            })
        PhoneCallData = []
        for PhoneCall, phoneCallDate in zip(phoneCalls, phoneCallDates):
            PhoneCallData.append({
            'PhoneCall': PhoneCall,
            'phoneCallDate': datetime.combine(datetime.strptime(phoneCallDate, '%Y-%m-%d').date(), time.min)
            })
        data = {'_id':user_id,'project':project,'subjectNumber':subjectNumber,'randomizeNumber':randomizeNumber,'group':group,'groupStudy':groupStudy,'ra':ra,'rn':rn,'status':status,'name':name,'hn':hn,'dob':dob,'phone':phone,'address':address,'parent':parent,'visit_data':visit_data,'PhoneCallData':PhoneCallData}
        db.update(data)
        flash('User profile updated successfully', 'success')
        db.stopClient()
        return redirect(url_for(last_page))
    return render_template('edit.html', user=user,last_page=last_page)

@app.route('/delete/<last_page>/<user_id>')
@login_required
def delete_user(user_id,last_page):
    db = funcMongoDB()
    db.connect_mongodb()
    db.delete(user_id)
    db.stopClient()
    flash('User profile deleted successfully', 'success')
    return redirect(url_for(last_page))

if __name__ == '__main__':
    app.run(debug=True)  # Set to False in production