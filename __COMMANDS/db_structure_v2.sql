CREATE DATABASE my_portal;

use my_portal;


/**
 * The students ID will be a sequence.
 * New inserted id will be like: 
 * [CURRENT_YEAR] + [(6 * '0') - (length_of_last_id + 1)] + [last_id + 1]
 *
*/
CREATE TABLE id_sequence (
	year INT PRIMARY KEY,
	next_id INT
);
-- Initialize the sequence with starting values for each year
INSERT INTO id_sequence (year, next_id) VALUES (2023, 1);

CREATE TABLE student (
	id VARCHAR(15) PRIMARY KEY,
	first_name nvarchar(50) NOT NULL,
	middle_name nvarchar(50) NOT NULL,
	last_name nvarchar(50) NOT NULL,
	date_of_birth DATE NOT NULL,
	email nvarchar(256) UNIQUE NOT NULL,
	password nvarchar(256) NOT NULL,
	email_verified BIT DEFAULT(0),
    profile_avatar nvarchar(256),
    gender varchar(6) DEFAULT('male')
);

DELIMITER //

CREATE TRIGGER before_student_insert
BEFORE INSERT ON student FOR EACH ROW
BEGIN
	DECLARE new_id VARCHAR(15);
	UPDATE id_sequence SET year = YEAR(CURDATE());
	SET new_id = CONCAT(YEAR(CURDATE()), LPAD((SELECT next_id FROM id_sequence WHERE year = YEAR(CURDATE())), 6, '0'));
	SET NEW.id = new_id;

	-- Update the next_id in the sequence table
	UPDATE id_sequence SET next_id = next_id + 1 WHERE year = YEAR(CURDATE());
END;

//
DELIMITER ;


CREATE TABLE teacher (
	id INT PRIMARY KEY AUTO_INCREMENT,
	first_name nvarchar(50) NOT NULL,
	last_name nvarchar(50) NOT NULL,
	date_of_birth DATE NOT NULL,
	email nvarchar(256) UNIQUE NOT NULL,
	password nvarchar(256) NOT NULL,
	email_verified BIT DEFAULT(0),
    profile_avatar nvarchar(256),
    gender varchar(6) DEFAULT('male')
);


CREATE TABLE subject (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name nvarchar(50) NOT NULL,
	code nvarchar(36) UNIQUE NOT NULL,
	created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE teacher_sub (
	primary_teacher BIT DEFAULT(0),
	teacher_id INT NOT NULL,
	sub_id INT NOT NULL,
	PRIMARY KEY  (teacher_id, sub_id),
	FOREIGN KEY (teacher_id) REFERENCES teacher(id),
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);


CREATE TABLE student_sub (
	student_id VARCHAR(15) NOT NULL,
	sub_id INT NOT NULL,
	PRIMARY KEY (student_id, sub_id),
	FOREIGN KEY (student_id) REFERENCES student(id),
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);


CREATE TABLE book (
	id INT PRIMARY KEY AUTO_INCREMENT,
	link nvarchar(256) NOT NULL,
	sub_id INT NOT NULL,
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);


CREATE TABLE lecture (
	id INT PRIMARY KEY AUTO_INCREMENT,
	title nvarchar(128),
	notes nvarchar(1024),
	sub_id INT NOT NULL,
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);


CREATE TABLE video (
	id INT PRIMARY KEY AUTO_INCREMENT,
	link nvarchar(256) NOT NULL,
	lec_id INT NOT NULL,
	FOREIGN KEY (lec_id) REFERENCES lecture(id) ON DELETE CASCADE,
	sub_id INT NOT NULL,
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);


CREATE TABLE pdfs(
	id INT PRIMARY KEY AUTO_INCREMENT,
	link nvarchar(256) NOT NULL,
	lec_id INT NOT NULL,
	FOREIGN KEY (lec_id) REFERENCES lecture(id) ON DELETE CASCADE,
	sub_id INT NOT NULL,
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);


CREATE TABLE grade(
	id INT PRIMARY KEY AUTO_INCREMENT,
	grade INT DEFAULT(0),
	student_id VARCHAR(15) NOT NULL,
	sub_id INT NOT NULL,
	FOREIGN KEY (student_id) REFERENCES student(id),
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);


CREATE TABLE quiz(
	id INT PRIMARY KEY AUTO_INCREMENT,
    description nvarchar(256),
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_time TIMESTAMP NOT NULL,
    duration INT NOT NULL,
    sub_id INT NOT NULL,
    FOREIGN KEY (sub_id) REFERENCES subject(id)
);


CREATE TABLE subject_ann_chat (
	id INT PRIMARY KEY AUTO_INCREMENT,
	message varchar(256) NOT NULL,
    message_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	teacher_id int(50) NOT NULL,
	sub_id INT NOT NULL,
	FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id)
);


CREATE TABLE chat_messages (
	id INT  PRIMARY KEY AUTO_INCREMENT,
    sub_id INT,
    user_id INT,
    role varchar(15),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sub_id) REFERENCES subject(id) ON DELETE CASCADE
);
