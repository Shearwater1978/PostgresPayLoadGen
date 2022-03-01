
DROP TABLE IF EXISTS person;

CREATE TABLE person (
    uuid VARCHAR ( 36 ) NOT NULL,
    fio VARCHAR ( 50 ) NOT NULL,
    phone VARCHAR ( 18 ) NOT NULL,
    age INT NOT NULL,
    addr VARCHAR ( 75 ) NOT NULL,
    email VARCHAR ( 75 ) NOT NULL
);
