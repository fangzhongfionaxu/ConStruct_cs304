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

@app.route('/browse/') #home
def browse():
    
    return render_template('browse_lookup.html',
                           page_title='Browsing Page')

@app.route('/login/') #home
def login():
    
    return render_template('login.html',
                           page_title='Login Page')

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

@app.route('/formecho/', methods=['GET','POST'])
def formecho():
    print("hi")
    if request.method == 'GET':
        return render_template('form_data.html',
                               page_title='Display of Form Data',
                               method=request.method,
                               form_data=request.args)
    elif request.method == 'POST':
        return render_template('form_data.html',
                               page_title='Display of Form Data',
                               method=request.method,
                               form_data=request.form)
    else:
        raise Exception('this cannot happen')

@app.route('/create_conf/', methods=['GET', 'POST'])
def create_conf():
    if request.method == 'POST':
        title = request.form.get('conf-title')
        description = request.form.get('conf-description')
        industry = request.form.get('conf-industry')
        location = request.form.get('conf-location')
        start_date = request.form.get('conf-start')
        end_date = request.form.get('conf-end')
        host = request.form.get('conf-host')
        if not title or not description or industry  == 'none' or not location or not start_date or not end_date or not host:
            flash("All fields are required to create a new conference")
            return render_template('create_conf.html')
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        curs.execute("select max(eid) from events")
        max_eid = curs.fetchone()[0]
        new_eid = (max_eid or 0) + 1
        curs.execute(
            "insert into events(eid,title,descript,industry,location,start_date,end_date,host) values (%s,%s,%s,%s,%s,%s,%s,%s)", (new_eid,title,description,industry,location,start_date,end_date,host))
        conn.commit()
        flash("Conference created successfully!")
        return redirect(url_for('create_conf'))
    return render_template('create_conf.html')


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'fx100_db' 
    print(f'will connect to {db_to_use}')
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
