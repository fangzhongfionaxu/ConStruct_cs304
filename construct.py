import cs304dbi as dbi
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


def select_conf(conn): #browse
    curs = dbi.dict_cursor(conn)
    sql = 'select * from movie where tt = %s'
    curs.execute(sql,[tt])
    result = curs.fetchone()
    if result:  
        flash("Cannot insert movie, ID already exist in database")
        return tt
    else:
        sql = 'insert into movie (tt, title, `release`, director, addedby) values (%s,%s, %s, %s, %s)'
        curs.execute(sql,[tt, title, year, director, 10027])
        conn.commit()
    return tt


def insert_user(conn, name, phnum, email, password, cid): #create_account page
    curs = dbi.dict_cursor(conn)
    sql = 'insert into users (name, phnum , email, password, cid) values (%s,%s,%s,%s,%s,%s )'
    curs.execute(sql,[name, phnum , email, password, cid])

def select_company(conn, cname):
    curs = dbi.dict_cursor(conn)
    select_c = 'select cid from companies where name like %s'
    cname = '%'+cname+'%'
    exist = curs.execute(select_c, [cname])
    if exist:
        return exist
    else:
        insert_c = 'insert into companies (cname, phnum , email, password, cid) values (%s,%s,%s,%s,%s,%s )'
        curs.execute(sql

def insert_conf(conn): #create_conf page