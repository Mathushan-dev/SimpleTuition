CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    email_address VARCHAR(50) NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    outstanding_questions VARCHAR(1024),
    completed_questions VARCHAR(1024)
);
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question VARCHAR(150) NOT NULL,
    keywords VARCHAR(150) NOT NULL,
    exam_id INTEGER NOT NULL
);