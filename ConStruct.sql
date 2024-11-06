use construct_db;
-- Fangzhong Xu and Ashley Cong
drop table if exists company;
drop table if exists attendees;
drop table if exists events;
drop table if exists users;


CREATE TABLE users  ( 

    uid  int, 
    name  varchar(40), 
    phnum  int,
    email varchar(40),
    password varchar(30),
    cid int,

    PRIMARY Key (uid)
)
ENGINE = InnoDB;

CREATE TABLE events  ( 

    eid  int, 
    title varchar(60), 
    desc varchar(200),
    host int, --is uid--[ref: > user.uid]
    industry enum('Academic','Energy',  'Materials', 'Industrials',  'Consumer Discretionary/Staples', 'Health Care', 
     'Financials', 'Information Technology', 'Real Estate',  'Communication Services', 'Utilities','Other') ,
    location varchar(100),
    start_date datetime,
    end_date datetime,

    PRIMARY Key (eid),
    index (title),
    foreign key (host) references user(uid)
        on update restrict
        on delete restrict --cannot delete this user if the user is hosting an event
)
ENGINE = InnoDB;

CREATE TABLE attendees(
    attendee int,
    eid int,
    checked_in bool,
    foreign key (eid) references event(eid)
        on update restrict
        on delete restrict
    foreign key (attendee) references user(uid)
        on update cascade
        on delete cascade
)
ENGINE = InnoDB;

CREATE TABLE companys(
    cid int,
    name varchar(50),
    
    PRIMARY KEY (cid),

    foreign key (cid) references user(cid)
        on update cascade
        on delete cascade

)
ENGINE = InnoDB;

