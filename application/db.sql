CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    email_address VARCHAR(50) NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    outstanding_questions VARCHAR(1024),
    completed_questions VARCHAR(1024),
    log VARCHAR(1024) NOT NULL
);
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question VARCHAR(1024) NOT NULL,
    keywords VARCHAR(1024) NOT NULL,
    exam_id VARCHAR(20) NOT NULL
);

UPDATE users
SET outstanding_questions = '1'
WHERE id = 2;