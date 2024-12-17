import cs304dbi as dbi
import bcrypt
import datetime
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


def select_conf(conn,query, industry): #select the conference based on industry or keyword
    curs = dbi.dict_cursor(conn)
    current_date = datetime.datetime.now()
    


    if query == "None" or query =="":
        query = False
    if industry == "none" or industry == "":
        industry = False

    if query and (industry is False):
        #Filter conferences based on the search
        query = f"%{query}%"
        sql = 'select  eid, title from events where title like %s or descript like %s'
        curs.execute(sql, (query, query))
        print (" use keyword")
        
    elif industry and (query is False):
        sql = 'select eid, title from events where industry like %s and end_date >= %s'
        curs.execute(sql, (industry, current_date))
        print (" use industry")
        
    elif query and industry:
        query = f"%{query}%"
        sql = 'select eid, title from events where industry like %s and (title like %s or descript like %s) and end_date >= %s'
        curs.execute(sql, (industry, query, query, current_date))
        print ("use both")
        
    else:
        sql = 'select eid, title from events where end_date >= %s'
        curs.execute(sql, (current_date))
        print (" show all")
    events = curs.fetchall()
    
    return events


def insert_conf(conn, title, descript, industry, location, start_date, end_date, host): #create a conf page and insert event into events
    curs = dbi.dict_cursor(conn)
    sql = 'insert into events(title,descript,industry,location,start_date,end_date,host) values (%s,%s,%s,%s,%s,%s,%s)'
    curs.execute(sql, [title,descript,industry,location,start_date,end_date,host])
    conn.commit()
    curs.execute('select last_insert_id() as last_id')
    new_event = curs.fetchone()
    new_eid = new_event['last_id']
    return new_eid

def get_conf(conn,eid): #get one conf from eid
    curs = dbi.dict_cursor(conn)
    sql = 'select * from events where eid = %s'
    curs.execute(sql, [eid])
    conference = curs.fetchone()
    return conference

def get_host(conn, eid):
    curs = dbi.dict_cursor(conn)
    sql = 'select host from events where eid = %s'
    curs.execute(sql, [eid])
    host = curs.fetchone()['host']
    return host


def get_conf_all(conn, query): #get all conf from title
    curs = dbi.dict_cursor(conn)
    event = "select title, eid from events where title like %s"
    curs.execute(event, ['%' + query + '%'])
    e = curs.fetchall()
    return e

def get_conf_by_user(conn,uid): #get all conf from one host
    curs = dbi.dict_cursor(conn)
    sql = 'select * from events where host = %s'
    curs.execute(sql, [uid])
    conference = curs.fetchall()
    return conference

def get_registered_conf(conn,uid):# get all conf(eid) registered by one user
    curs = dbi.dict_cursor(conn)
    sql = 'select * from attendees where aid = %s'
    curs.execute(sql, [uid])
    conferences = curs.fetchall()
    result = []
    for conf in conferences:
        eid = conf['eid']
        sql1 = 'select * from events where eid = %s'
        curs.execute(sql1,[eid])
        result.append(curs.fetchone())

    return result

def update_user(conn, uid, name, phnum, email, cid): #update user information in database
    curs = dbi.dict_cursor(conn)
    sql = 'update users set name = %s, phnum = %s, email = %s, cid = %s where uid = %s'
    curs.execute(sql, [name, phnum, email, cid, uid])
    conn.commit()

def insert_user(conn, name, phnum, email, password, cname): #create_account page, return new uid
    curs = dbi.dict_cursor(conn)
    cid = insert_or_get_cid(conn, cname)
    print(cid, type(cid))
    

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    stored = hashed.decode('utf-8')
    sql = 'insert into users (name, phnum , email, hashedpswd, cid) values (%s,%s,%s,%s,%s )'
    sql2 = 'select last_insert_id() as uid'
    curs.execute(sql,[name, phnum , email, stored, cid])
    conn.commit()

    curs.execute(sql2)
    row = curs.fetchone()
    uid = row['uid']

    return uid


def insert_or_get_cid(conn, cname): #insert new company if input company does not exist, select cid if it does; return new cid
    curs = dbi.dict_cursor(conn)
    select_c = 'select cid from companies where name like %s'
    curs.execute(select_c, ['%'+cname+'%'])
    exist = curs.fetchone()
    if exist:
        return exist['cid']
    else:
        insert = 'insert into companies (name) values (%s )'
        curs.execute(insert,[cname])
        conn.commit()
        curs.execute("select last_insert_id() as cid")
        row = curs.fetchone()
        cid = row['cid']
        return cid

def get_user(conn,uid):
    curs = dbi.dict_cursor(conn)
    sql = 'select u.uid, u.name, u.phnum, u.email,  c.name from users u, companies c where uid = %s' #took out  and c.cid = u.cid
    curs.execute(sql, uid)
    user = curs.fetchone()
    
    return user
    

def user_exist(conn,email): #loggin information exist
    curs = dbi.dict_cursor(conn)
    sql = "select uid, email, hashedpswd from users where email like %s"
    curs.execute(sql, email)
    user = curs.fetchone()
    return user

def register_conf(conn,eid,aid): #add one eid aid pair to attendees
    curs = dbi.dict_cursor(conn)
    sql = '''INSERT INTO attendees (eid, aid, checked_in )
            VALUES (%s,%s, false) ON DUPLICATE KEY UPDATE eid = %s ;'''
    curs.execute(sql,[eid,aid,eid])
    conn.commit()
    return 

def get_num_registered(conn,eid):
    #calculate the number of attendees in this conference
    curs = dbi.dict_cursor(conn)
    sql1 = '''SELECT COUNT(aid) AS num_rows
            FROM attendees
            WHERE eid = %s'''
    curs.execute(sql1,eid)
    num_registered = curs.fetchone()['num_rows']
    return num_registered


