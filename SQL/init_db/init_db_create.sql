
drop table if exists person;

CREATE TABLE person (
    fio VARCHAR ( 50 ) NOT NULL,
    phone VARCHAR ( 18 ) NOT NULL,
    age INT NOT NULL,
    city VARCHAR ( 50 ) NOT NULL,
    addr VARCHAR ( 75 ) NOT NULL,
    inn BIGINT
);
