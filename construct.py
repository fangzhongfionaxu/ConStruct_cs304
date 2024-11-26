import cs304dbi as dbi

def select_conf(conn): #browse
    curs = dbi.dict_cursor(conn)
    sql = 'select * from movie where tt = %s'
    curs.execute(sql,[tt])
    result = curs.fetchone()
    if result:  
        flash("Cannot insert movie, ID already exist in database")
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

def get_eid(conn,eid):
    curs = dbi.dict_cursor(conn)
    sql = 'select eid,title,descript,industry,location,start_date,end_date,host from events where eid = %s'
    curs.execute(sql,[eid])
    conn.commit()
    return curs.fetchone()