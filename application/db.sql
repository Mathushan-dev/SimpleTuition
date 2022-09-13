CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    email_address VARCHAR(40) NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    outstanding_questions VARCHAR(350),
    completed_questions VARCHAR(350),
    log VARCHAR(500) NOT NULL
);
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question VARCHAR(250) NOT NULL,
    keywords VARCHAR(250) NOT NULL,
    exam_id VARCHAR(20) NOT NULL
);

INSERT INTO questions (id, question, keywords, exam_id)
VALUES (1, 'What is a cell?', '[[["small cells", "tiny cells"], ["cell wall", "cell membrane"]], [["nucleus"], ["DNA", "genetic material"]]]', 1);

INSERT INTO users (username, email_address, password_hash, outstanding_questions, completed_questions, log)
VALUES ('nirusa98', 'mathiyalaganmathushan@gamil.com', '$2b$12$xd8ApXCvqUAL.v0zhm3HU.UvXCiLpiRPCD6oCAzzJVJhoyiieih26', NULL, NULL, 'Account created on 08/23/2022, 16:52:33');

UPDATE users
SET outstanding_questions = '1'
WHERE id = 2;