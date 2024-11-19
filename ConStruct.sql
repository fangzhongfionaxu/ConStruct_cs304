use construct_db;
-- Fangzhong Xu and Ashley Cong
drop table if exists companies;
drop table if exists attendees;
drop table if exists events;
drop table if exists users;


CREATE TABLE users  ( 

    uid int, 
    name varchar(40), 
    phnum int,
    email varchar(40),
    password varchar(30),
    cid int,

    PRIMARY Key (uid)
)
ENGINE = InnoDB;

CREATE TABLE events  ( 

    eid  int, 
    title varchar(60), 
    descript varchar(1000),
    host int, -- is uid--[ref: > user.uid]
    industry enum('Academic','Energy',  'Materials', 'Industrials',  'Consumer Discretionary/Staples', 'Health Care', 
     'Financials', 'Information Technology', 'Real Estate',  'Communication Services', 'Utilities','Other') ,
    location varchar(100),
    start_date datetime, -- check if format fits
    end_date datetime,

    PRIMARY Key (eid),
    index (title),
    foreign key (host) references users(uid)
        on update restrict
        on delete restrict -- cannot delete this user if the user is hosting an event
)
ENGINE = InnoDB;

CREATE TABLE attendees(
    eid int,
    aid int, -- attendee
    checked_in boolean,
    foreign key (eid) references events(eid)
        on update restrict
        on delete restrict
    foreign key (aid) references users(uid)
        on update cascade
        on delete cascade
)
ENGINE = InnoDB;

CREATE TABLE companies(
    cid int,
    name varchar(100),
    
    PRIMARY KEY (cid),

    foreign key (cid) references users(cid)
<<<<<<< HEAD

        on update cascade
        on delete cascade
=======
        on update restrict
        on delete restrict
>>>>>>> fa35a463f184dd13d58c1e1b91caa646b6c4aecc

)
ENGINE = InnoDB;