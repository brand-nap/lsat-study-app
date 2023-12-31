BEGIN TRANSACTION;

DROP TABLE IF EXISTS users, tests, scores, sections, section_types, prompts, questions, answers;

CREATE TABLE users (
	user_id SERIAL,
	username varchar(50) NOT NULL UNIQUE,
	password_hash varchar(200) NOT NULL,
	role varchar(50) NOT NULL,
	CONSTRAINT PK_user PRIMARY KEY (user_id)
);
CREATE TABLE tests (
    test_id SERIAL PRIMARY KEY,
    exam_date date,
);
CREATE TABLE scores (
    score_id SERIAL PRIMARY KEY,
    test_id int REFERENCES tests(test_id),
    raw_score int,
    lsat_score int
);
CREATE TABLE sections (
    section_id int PRIMARY KEY,
    test_id REFERENCES tests(test_id),
    type_id REFERENCES section_types(type_id)
    total_questions int
);
CREATE TABLE section_types (
    type_id int PRIMARY KEY,
    name varchar,
    directions varchar,
);
CREATE TABLE prompts (
    prompt_id int PRIMARY KEY,
    type_id int REFERENCES section_types(type_id),
    content varchar
);
CREATE TABLE conditions (
    condition_id SERIAL PRIMARY KEY,
    prompt_id int REFERENCES prompts(prompt_id),
    content varchar
)

CREATE TABLE questions (
    question_id int PRIMARY KEY,
    prompt_id int REFERENCES prompts(prompt_id),
    content varchar
);

CREATE TABLE answers(
    answer_id SERIAL PRIMARY KEY,
    question_id int NOT NULL REFERENCES questions(question_id),
    content varchar,
    is_correct boolean
);


COMMIT TRANSACTION;
