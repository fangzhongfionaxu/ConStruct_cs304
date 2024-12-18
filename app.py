from flask import (Flask, render_template, make_response, url_for, request, 
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import bcrypt
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
    if 'uid' in session:
        uid = session['uid']
    else:
        uid = 0
        flash('please login or create account')

    return render_template('main.html',
                           page_title='Main Page',
                           uid = uid)



@app.route('/browse/', defaults={'uid': None}, methods=["GET"])
@app.route('/browse/<uid>', methods = ["GET"]) #home
def browse(uid):
    query = request.args.get('query')
    industry = request.args.get('conf-industry')
    print(query)
    print(industry)
    
    if 'uid' not in session:
        flash('You are not logged in. Please login or create account')
        return redirect(url_for('home'))

    uid = session['uid']
    
    conn = dbi.connect()
    events = c.select_conf(conn,query, industry)
    sessvalue = request.cookies.get('session')
    print (sessvalue)
    length = len(events)
    
    return render_template('browse_lookup.html', page_title= "Browsing Page" , uid = uid , e=events, query=query, industry= industry, length=length)


    

@app.route('/login/', methods = ['GET','POST']) #home
def login():
    if request.method == 'GET':
        return render_template('login.html', page_title = 'Login Page')
    
    if request.method == 'POST':
        conn= dbi.connect()
        
        email = request.form.get('email')
        password = request.form.get('password')
        user = c.user_exist(conn,email) 
        if user is None:
            flash('user does not exist, please re-enter email')
            return render_template('login.html',
                                page_title='Login Page')
        else:
            stored = user['hashedpswd']
            hashed2 = bcrypt.hashpw(password.encode('utf-8'),
                                        stored.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            if hashed2_str == stored:
                print('loggin info match!')
                flash('successfully logged in as ' + email )

                session['email'] = user['email']
                session['uid'] = user['uid']
                session['logged_in'] = True

                return redirect( url_for('browse', uid=session['uid']) )
            else:
                flash('login incorrect. Try again or join')
                return redirect( url_for('home'))
            
@app.route('/logout/', methods = ['GET','POST']) #home
def logout():
    if 'uid' in session:
        
        session.pop('uid')
        session.pop('email')
        session.pop('logged_in')
        flash('You are logged out')
        return redirect(url_for('home'))
    else:
        flash('you are not logged in. Please login or create account')
        return redirect( url_for('home') )

@app.route('/create_account/', methods=['GET','POST']) #add user to users table
def create_account():
    
    if request.method == 'GET':
        return render_template('create_account.html',  
                                  
                           page_title='Create Account Page')

    elif request.method == 'POST':
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        name = request.form.get('name')
        phnum = request.form.get('phnum')
        email = request.form.get('email')
        password = request.form.get('password1')
        password2 = request.form.get('password2')

        user_exist = '''select uid from users where email like %s ''' # if email is already used, flash
        curs.execute(user_exist,[email])
        exist = curs.fetchone()
        if exist: 
            flash('user already exist, change email')
            return render_template('create_account.html',page_title='Create Account Page')
        if password!= password2:
            flash('passwords do not match, please check ')
            return redirect( url_for('create_account'))
        if not name or not phnum or not email or not password or not password2:
            flash("All fields are required to create a new account")
            return render_template('create_account.html',page_title='Create Account Page')
        new_uid = c.insert_user(conn, name, phnum, email, password) #when we have the login page, will redirect to loggedin browsing page
        flash('New account created successfully')
        sql = 'select uid, name, phnum, email, cid from users where email like %s'
        curs.execute(sql,[email])
        user = curs.fetchone()
        session['email'] = user['email']
        session['uid'] = user['uid']
    
        session['logged_in'] = True
        session['visits'] = 1

        return redirect(url_for('account_detail',title ='Account Detail Page',uid = new_uid)) #redirect to user detail page


@app.route('/account_detail/<uid>', methods=['GET','POST']) #user detail (account detail) page, update with post
def account_detail(uid):
    if 'uid' not in session:
        flash('You are not logged in. Please login or create account')
        return redirect(url_for('home'))


    uid = session['uid']
    print (uid)
    conn = dbi.connect()

    #conferences = c.get_conf_by_user(conn, uid)
    if request.method == 'POST':
        name = request.form.get('name')
        phnum = request.form.get('phnum')
        email = request.form.get('email')
        print(name )
        print("test if it goes to post and update")
        c.update_user(conn, uid, name, phnum, email)
        flash("Your account information has been updated!")
        return redirect(url_for('account_detail',title ='Account Detail Page', uid=uid))
    
    user = c.get_user(conn,uid)
    conferences = c.get_registered_conf(conn,uid)

    if not user:
        flash("User not found. Redirecting to create account page.")
        return redirect(url_for('create_account'))
    return render_template('account_detail.html',title ='Account Detail Page', user=user,uid = uid, conferences = conferences)


#@app.route('/create_conf/<uid>', defaults={'uid': None}, methods=["POST"])
@app.route('/create_conf/<uid>', methods=['GET','POST'])
def create_conf(uid):
    
    if 'uid' in session:
        
        uid = session['uid']
        email = session['email']
        if request.method == 'GET':
            return render_template('create_conf.html', uid = uid, email = email)
        if request.method == 'POST':
            title = request.form.get('conf-title')
            descript = request.form.get('conf-description')
            industry = request.form.get('conf-industry')
            location = request.form.get('conf-location')
            start_date = request.form.get('conf-start')
            end_date = request.form.get('conf-end')
            host = uid

            if not title or not descript or industry  == 'none' or not location or not start_date or not end_date :
                flash("All fields are required to create a new conference")
                return render_template('create_conf.html')
            
            conn = dbi.connect()
            new_eid = c.insert_conf(conn, title, descript,industry,location,start_date,end_date,host)
            flash("Conference created successfully!")
            return redirect(url_for('conf_detail', eid=new_eid)) # go to conf detail page
        
    else:
        flash('You are not logged in. Please login or create account before creating conference')
        return redirect(url_for('home'))

@app.route('/conf_detail/<eid>', methods=['GET', 'POST'])
def conf_detail(eid):
    conn = dbi.connect()
    conference = c.get_conf(conn,eid)
    host = c.get_host(conn,eid)
    if 'uid' in session:
        aid = session['uid']
        num = c.get_num_registered(conn,eid)
        
    else:
        aid = 0
        flash('please login or create account')
        return redirect(url_for('home'))
    
    if not conference:
        flash("Conference with eid=%s not found. Redirecting to create conference page." %eid)
        return redirect(url_for('create_conf', uid = host))
    
    if request.method=='POST':
        if 'uid' in session:
            aid = session['uid']
            
            c.register_conf(conn,eid,aid)
            num = c.get_num_registered(conn,eid)
    
    
    return render_template('conf_detail.html',**conference, num = num, aid = aid,uid = aid)
    



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
