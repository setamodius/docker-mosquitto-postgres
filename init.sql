DROP TABLE IF EXISTS users;

create table users (id SERIAL PRIMARY KEY, username VARCHAR(25) NOT NULL, password VARCHAR(128) NOT NULL, super smallint NOT NULL DEFAULT 0);
CREATE UNIQUE INDEX users_username ON users (username);

insert into users(username, password, super) values('admin', 'PBKDF2$sha1$98$XaIs9vQgmLujKHZG4/B3dNTbeP2PyaVKySTirZznBrE=$2DX/HZDTojVbfgAIdozBi6CihjWP1+akYnh/h9uQfIVl6pLoAiwJe1ey2WW2BnT+', 1);


DROP TABLE IF EXISTS acls;
CREATE TABLE acls (id SERIAL PRIMARY KEY, username VARCHAR(25) NOT NULL, topic VARCHAR(256) NOT NULL, acc smallint NOT NULL DEFAULT 1);

CREATE UNIQUE INDEX acls_user_topic ON acls (username, topic);

INSERT INTO acls (username, topic, acc) VALUES ('admin', 'read/+', 1);
INSERT INTO acls (username, topic, acc) VALUES ('admin', 'write/+', 2);
INSERT INTO acls (username, topic, acc) VALUES ('admin', 'both/+', 3);
