DROP TABLE IF EXISTS users;

create table users (id SERIAL PRIMARY KEY, username VARCHAR(25) NOT NULL, password VARCHAR(128) NOT NULL, name VARCHAR(128) NOT NULL, privilege int NOT NULL, super smallint NOT NULL DEFAULT 0);
CREATE UNIQUE INDEX users_username ON users (username);

insert into users(username, password, name, privilege, super) values('master', 'PBKDF2$sha256$10000$3YA/d8uocGb7X6FP$xXqfJgnX7H651ZQTwpVnwrg2ODIOvla+', 'Master User', 252, 1);


DROP TABLE IF EXISTS acls;
CREATE TABLE acls (id SERIAL PRIMARY KEY, privilege int NOT NULL, topic VARCHAR(256) NOT NULL, acc smallint NOT NULL DEFAULT 1);

CREATE UNIQUE INDEX acls_user_topic ON acls (privilege, topic);

INSERT INTO acls (privilege, topic, acc) VALUES (252, 'read/+', 1);
INSERT INTO acls (privilege, topic, acc) VALUES (252, 'write/+', 2);

