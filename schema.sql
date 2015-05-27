DROP TABLE IF EXISTS go_users CASCADE;
CREATE TABLE go_users (
    userid    bigint PRIMARY KEY,
    username  text,
    fullname  text,
    password  text,
    email     text
);

DROP TABLE IF EXISTS go_places CASCADE;
CREATE TABLE go_places (
    placeid    bigint PRIMARY KEY,
    placename  text,
    latitude   float,
    longitude  float
);

DROP TABLE IF EXISTS go_visits CASCADE;
CREATE TABLE go_visits (
    visitid  bigint PRIMARY KEY,
    userid   bigint REFERENCES go_users(userid),
    placeid  bigint REFERENCES go_places(placeid),
    note     text
);

DROP TABLE IF EXISTS go_notes CASCADE;
CREATE TABLE go_notes (
    noteid       bigint PRIMARY KEY,
    placeid      bigint REFERENCES go_places(placeid),
    authorid     bigint REFERENCES go_users(userid),
    recipientid  bigint REFERENCES go_users(userid),
    body         text,
    ispublic     boolean,
    photo        text
);

