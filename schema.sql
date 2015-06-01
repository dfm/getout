DROP TABLE IF EXISTS go_users CASCADE;
CREATE TABLE go_users (
    userid     bigint PRIMARY KEY,
    username   text,
    fullname   text,
    bio        text,
    password   text,
    email      text,
    location   text,
    avatarurl  text
);

DROP TABLE IF EXISTS go_locations CASCADE;
CREATE TABLE go_locations (
    locationid    bigint PRIMARY KEY,
    locationname  text,
    latitude      float,
    longitude     float
);

DROP TABLE IF EXISTS go_visits CASCADE;
CREATE TABLE go_visits (
    visitid     bigint PRIMARY KEY,
    userid      bigint REFERENCES go_users(userid),
    locationid  bigint REFERENCES go_locations(locationid),
    timestamp   timestamp,
    body        text
);

DROP TABLE IF EXISTS go_comments CASCADE;
CREATE TABLE go_comments (
    commentid  bigint PRIMARY KEY,
    visitid    bigint REFERENCES go_visits(visitid),
    authorid   bigint REFERENCES go_users(userid),
    timestamp  timestamp,
    body       text
);

DROP TABLE IF EXISTS go_visit_likes CASCADE;
CREATE TABLE go_visit_likes (
    likeid     bigint PRIMARY KEY,
    visitid    bigint REFERENCES go_visits(visitid),
    likerid    bigint REFERENCES go_users(userid),
    timestamp  timestamp
);

DROP TABLE IF EXISTS go_location_likes CASCADE;
CREATE TABLE go_location_likes (
    likeid      bigint PRIMARY KEY,
    locationid  bigint REFERENCES go_locations(locationid),
    likerid     bigint REFERENCES go_users(userid),
    timestamp   timestamp
);

DROP TABLE IF EXISTS go_notes CASCADE;
CREATE TABLE go_notes (
    noteid       bigint PRIMARY KEY,
    locationid   bigint REFERENCES go_locations(locationid),
    authorid     bigint REFERENCES go_users(userid),
    recipientid  bigint REFERENCES go_users(userid),
    timestamp    timestamp,
    body         text,
    ispublic     boolean,
    photourl     text
);
