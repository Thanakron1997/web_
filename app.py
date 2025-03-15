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
    db = funcMongoDB()
    ongoing_project = ['test']
    all_project = {}
    for i in ongoing_project:
        i_data = {}
        db.connect_mongodb(collectionName = i)
        users = db.get_data()
        contiune_status = [entry for entry in users if entry['status'] == 'C']
        wd_status = [entry for entry in users if entry['status'] == 'WD']
        sf_status = [entry for entry in users if entry['status'] == 'SF']
        finish_status = [entry for entry in users if entry['status'] == 'Finish']
        lost_status = [entry for entry in users if entry['status'] == 'Lost F/U']
        trans_status = [entry for entry in users if entry['status'] == 'Transfer']
        i_data['total'] = len(users)
        i_data['wd'] = len(wd_status)
        i_data['continue'] = len(contiune_status)
        i_data['sf'] = len(sf_status)
        i_data['finish'] = len(finish_status)
        i_data['lost'] = len(lost_status)
        i_data['transfer'] = len(trans_status)
        all_project[i] = i_data
    db.stopClient()
    return render_template('index.html',data=all_project)

@app.route('/project1')
@login_required
def project1():
    db = funcMongoDB()
    db.connect_mongodb(collectionName = 'test')
    users = db.get_data()
    db.stopClient()
    users = updateNextVist(users) 
    return render_template('project1.html', users=users)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        db = funcMongoDB()
        db.connect_mongodb()
        query_key = request.form['query_key']
        query_val = request.form['query_val']
        query = {query_key:query_val}
        result = db.searchall(query)
        db.stopClient()
        if len(result)>0:
            result = updateNextVist(result)
        else:
            result = "No Data"
    else:
        result = None
    return render_template('search.html', users=result)

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
        notes_visits = request.form.getlist('notes')
        visit_data= []
        for visit, visit_date, next_visit,next_visit_date,note_visit in zip(visits, visit_dates, next_visits,next_visit_dates,notes_visits):
            visit_data.append({
                'visit': visit,
        'visit_date': datetime.combine(datetime.strptime(visit_date, '%Y-%m-%d').date(), time.min),  # Convert to datetime
        'next_visit': next_visit,
        'next_visit_date': "NA" if next_visit_date == "" else datetime.combine(datetime.strptime(next_visit_date, '%Y-%m-%d').date(), time.min),  # Convert to datetime
        'notes':note_visit,
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
        notes_visits = request.form.getlist('notes')
        visit_data= []
        for visit, visit_date, next_visit,next_visit_date,note_visit in zip(visits, visit_dates, next_visits,next_visit_dates,notes_visits):
            visit_data.append({
        'visit': visit,
        'visit_date': datetime.combine(datetime.strptime(visit_date, '%Y-%m-%d').date(), time.min),  # Convert to datetime
        'next_visit': next_visit,
        'next_visit_date': "NA" if next_visit_date == "" else datetime.combine(datetime.strptime(next_visit_date, '%Y-%m-%d').date(), time.min),  # Convert to datetime
        'notes':note_visit,
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
    app.run(host='0.0.0.0',port="8088",debug=True)  # Set to False in production