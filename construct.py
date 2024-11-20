import cs304dbi as dbi

def select_conf(conn):
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