import cs304dbi as dbi
import bcrypt
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


def select_conf(conn,query, industry): #select the number of 
    curs = dbi.dict_cursor(conn)
    if query == "None" or query =="":
        query = False
    if industry == "none" or industry == "":
        industry = False

    if query and (industry is False):
        #Filter conferences based on the search
        query = f"%{query}%"
        sql = 'select * from events where title like %s or descript like %s'
        curs.execute(sql, (query, query))
        print (" use keyword")
        
    elif industry and (query is False):
        sql = 'select * from events where industry like %s'
        curs.execute(sql, (industry,))
        print (" use industry")
        
    elif query and industry:
        query = f"%{query}%"
        sql = 'select * from events where industry like %s and (title like %s or descript like %s)'
        curs.execute(sql, (industry, query, query))
        print ("use both")
        
    else:
        curs.execute("select * from events")
        print ("show all")
    events = curs.fetchall()
    
    return events


def insert_conf(conn, title, descript, industry, location, start_date, end_date, host): #create_conf page
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

def get_conf_all(conn, query): #get all conf from title
    curs = dbi.dict_cursor(conn)
    event = "select title, eid from events where title like %s"
    curs.execute(event, ['%' + query + '%'])
    e = curs.fetchall()
    return e

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
    sql = 'select u.uid, u.name, u.phnum, u.email,  c.name from users u, companies c where uid = %s and c.cid = u.cid'
    curs.execute(sql, uid)
    user = curs.fetchone()
    
    return user
    

def user_exist(conn,email): #loggin information exist
    curs = dbi.dict_cursor(conn)
    sql = "select uid, email, hashedpswd from users where email like %s"
    curs.execute(sql, email)
    user = curs.fetchone()
    return user
