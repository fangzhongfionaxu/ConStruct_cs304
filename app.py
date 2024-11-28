from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi
import construct as c
import secrets
dbi.conf('construct_db')

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = secrets.token_hex()

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True


@app.route('/') #home
def home():
    return render_template('main.html',
                           page_title='Main Page')

# You will probably not need the routes below, but they are here
# just in case. Please delete them if you are not using them


@app.route('/greet/', methods=["GET", "POST"])
def greet():
    if request.method == 'GET':
        return render_template('greet.html',
                               page_title='Form to collect username')
    else:
        try:
            username = request.form['username'] # throws error if there's trouble
            flash('form submission successful')
            return render_template('greet.html',
                                   page_title='Welcome '+username,
                                   name=username)

        except Exception as err:
            flash('form submission error'+str(err))
            return redirect( url_for('index') )

# This route displays all the data from the submitted form onto the rendered page



@app.route('/browse/') #home
def browse():
    
    return render_template('browse_lookup.html',
                           page_title='Browsing Page')

@app.route('/login/') #home
def login():
    
    return render_template('login.html',
                           page_title='Login Page')


@app.route('/create_account/', methods=['GET','POST']) #home
def create_account():
    conn = dbi.connect()
    if request.method == 'GET':
        return render_template('create_account.html',  
                                  
                           page_title='Create Account Page')

    elif request.method == 'POST':
        name = request.form.get('name')
        phnum = request.form.get('phnum')
        email = request.form.get('email')
        password = request.form.get('password')
        cname = request.form.get('company')
        uid = c.insert_user(conn, name, phnum, email, password, cname) #when we have the login page, will redirect to loggedin browsing page

        return redirect(url_for('home')) #redirect to user account page
""" def user_detail(uid):
 """    
@app.route('/account_detail/<uid>', methods=['GET','POST']) #home
def account_detail(uid):
    conn = dbi.connect()
    conference = c.get_eid(conn,eid)
    if not conference:
        flash("Conference with eid=%s not found. Redirecting to create conference page." %eid)
        return redirect(url_for('create_conf'))
    return render_template('conf_detail.html',**conference)
    return render_template('account_detail.html',
                           title = 'Account Detail Page')

@app.route('/create_conf/', methods=['GET', 'POST'])
def create_conf():
    if request.method == 'POST':
        title = request.form.get('conf-title')
        descript = request.form.get('conf-description')
        industry = request.form.get('conf-industry')
        location = request.form.get('conf-location')
        start_date = request.form.get('conf-start')
        end_date = request.form.get('conf-end')
        host = request.form.get('conf-host')
        if not title or not descript or industry  == 'none' or not location or not start_date or not end_date or not host:
            flash("All fields are required to create a new conference")
            return render_template('create_conf.html')
        conn = dbi.connect()
        new_eid = c.insert_conf(conn, title, descript,industry,location,start_date,end_date,host)
        flash("Conference created successfully!")
        return redirect(url_for('conf_detail', eid=new_eid)) # go to conf detail page
    return render_template('create_conf.html')

@app.route('/conf_detail/<eid>', methods=['GET', 'POST'])
def conf_detail(eid):
    conn = dbi.connect()
    conference = c.get_eid(conn,eid)
    if not conference:
        flash("Conference with eid=%s not found. Redirecting to create conference page." %eid)
        return redirect(url_for('create_conf'))
    return render_template('conf_detail.html',**conference)
    



if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'construct_db' 
    print(f'will connect to {db_to_use}')
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
