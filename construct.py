import cs304dbi as dbi
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


def select_conf(conn): #browse not done yet
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

def insert_conf(conn, title, descript, industry, location, start_date, end_date, host): #create_conf page
    curs = dbi.dict_cursor(conn)
    sql = 'insert into events(title,descript,industry,location,start_date,end_date,host) values (%s,%s,%s,%s,%s,%s,%s)'
    """ curs.execute("select max(eid) from events")
    max_eid = curs.fetchone()[0]
    new_eid = (max_eid or 0) + 1 """
    curs.execute(sql, [title,descript,industry,location,start_date,end_date,host])
    conn.commit()
    curs.execut('select last_insert_id()')
    new_event = curs.fetchone()
    new_eid = new_event[0]
    return new_eid



def insert_user(conn, name, phnum, email, password, cname): #create_account page, return new uid
    curs = dbi.dict_cursor(conn)
    cid = insert_or_get_cid(conn, cname)
    print(cid, type(cid))
    sql = 'insert into users (name, phnum , email, password, cid) values (%s,%s,%s,%s,%s )'
    sql2 = 'select last_insert_id() as uid'
    curs.execute(sql,[name, phnum , email, password, cid])
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

