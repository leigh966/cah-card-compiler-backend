DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS contributers;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS sessions;

CREATE TABLE groups (
    group_id CHAR(36) PRIMARY KEY,
    group_name VARCHAR(20) NOT NULL
);

CREATE TABLE contributers (
    contributer_id BIGINT PRIMARY KEY,
    password_hash VARCHAR(100) NOT NULL,
    contributer_name VARCHAR(20) NOT NULL,
    group_id CHAR(36) NOT NULL,
    FOREIGN KEY(group_id) REFERENCES groups(group_id)
);

CREATE TABLE cards (
    card_id BIGINT PRIMARY KEY,
    card_text VARCHAR(50) NOT NULL,
    contributer_id BIGINT NOT NULL,
    FOREIGN KEY(contributer_id) REFERENCES contributers(contributer_id)
);

CREATE TABLE sessions (
    session_id CHAR(36) PRIMARY KEY,
    contributer_id BIGINT NOT NULL,
    FOREIGN KEY(contributer_id) REFERENCES contributers(contributer_id)
);