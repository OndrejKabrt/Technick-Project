CREATE DATABASE kabrt;
USE kabrt;

CREATE TABLE Teacher (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    teacher_username VARCHAR(20) NOT NULL UNIQUE,
    teacher_password VARCHAR(25) NOT NULL,
    email VARCHAR(30) NOT NULL CHECK (email LIKE '%@%'),
    phone_number VARCHAR(13) NOT NULL
);

CREATE TABLE Subject (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(30) NOT NULL,
    subject_description VARCHAR(50)
);

CREATE TABLE Class (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL,
    grade INT NOT NULL CHECK (grade BETWEEN 1 AND 4),
    number_of_class INT NOT NULL CHECK (number_of_class >= 0),
    year_of_entry DATE NOT NULL,
    active BIT NOT NULL,
    Class_Teacher_ID INT,
    FOREIGN KEY (Class_Teacher_ID) REFERENCES Teacher(id) ON DELETE SET NULL
);

CREATE TABLE Student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    user_password VARCHAR(20) NOT NULL,
    number_in_class_order INT NOT NULL,
    is_student BIT NOT NULL,
    Class_ID INT,
    FOREIGN KEY (Class_ID) REFERENCES Class(id) ON DELETE SET NULL
);

CREATE TABLE Student_Card (
    id INT PRIMARY KEY AUTO_INCREMENT,
    town VARCHAR(15) NOT NULL,
    street VARCHAR(20) NOT NULL,
    descriptive_number VARCHAR(10) NOT NULL,
    zip_code VARCHAR(6) NOT NULL,
    email VARCHAR(30) NOT NULL CHECK (email LIKE '%@%'),
    date_of_birth DATE NOT NULL,
    phone_number VARCHAR(13),
    Student_ID INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(id) ON DELETE CASCADE
);

CREATE TABLE Course (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(40) NOT NULL,
    number_of_theor_hours INT NOT NULL CHECK (number_of_theor_hours >= 0),
    number_of_practic_hours INT NOT NULL CHECK (number_of_practic_hours >= 0),
    Student_ID INT,
    Teacher_ID INT,
    Subject_ID INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(id) ON DELETE CASCADE,
    FOREIGN KEY (Teacher_ID) REFERENCES Teacher(id) ON DELETE SET NULL,
    FOREIGN KEY (Subject_ID) REFERENCES Subject(id) ON DELETE SET NULL
);

CREATE TABLE Grade (
    id INT PRIMARY KEY AUTO_INCREMENT,
    grade INT NOT NULL CHECK (grade BETWEEN 1 AND 5),
    description VARCHAR(25),
    date_of_award DATE,
    Course_ID INT,
    FOREIGN KEY (Course_ID) REFERENCES Course(id) ON DELETE CASCADE
);

CREATE TABLE Certificate (
    id INT PRIMARY KEY AUTO_INCREMENT,
    certificate_name VARCHAR(80) NOT NULL,
    issuing_organization VARCHAR(50),
    description VARCHAR(80)
);

CREATE TABLE Own (
    id INT PRIMARY KEY AUTO_INCREMENT,
    valid_since DATE NOT NULL,
    valid_to DATE,
    Ucitel_ID INT,
    Certifikat_ID INT,
    FOREIGN KEY (Ucitel_ID) REFERENCES Teacher(id) ON DELETE CASCADE,
    FOREIGN KEY (Certifikat_ID) REFERENCES Certificate(id) ON DELETE CASCADE
);




-- View for listing active students
CREATE VIEW list_of_active_students AS
SELECT Student.first_name, Student.last_name, Class.name
FROM Student 
INNER JOIN Class ON Student.Class_ID = Class.id
WHERE Student.is_student = 1;

-- View for counting students in a class
CREATE VIEW count_of_class_students AS
SELECT Class.name, Class.number_of_class, COUNT(*) AS Pocet_Studentu
FROM Student
INNER JOIN Class ON Student.Class_ID = Class.id
WHERE Student.is_student = 1
GROUP BY Class.name, Class.number_of_class;

-- View for listing courses and enrolled students
CREATE VIEW course_students AS
SELECT Course.course_name, CONCAT(Student.first_name, ' ', Student.last_name) AS Student
FROM Course
INNER JOIN Student ON Course.Student_ID = Student.id;

-- View for listing teachers and their certificates
CREATE VIEW teachers_certificate AS
SELECT CONCAT(Teacher.first_name, ' ', Teacher.last_name) AS Teacher, Certificate.certificate_name
FROM Own
INNER JOIN Teacher ON Own.Ucitel_ID = Teacher.id
INNER JOIN Certificate ON Own.Certifikat_ID = Certificate.id;

-- View for listing teachers and their courses
CREATE VIEW courses_and_teachers AS
SELECT DISTINCT Subject.subject_name, CONCAT(Teacher.first_name, ' ', Teacher.last_name) AS Teacher
FROM Course
INNER JOIN Teacher ON Course.Teacher_ID = Teacher.id
INNER JOIN Subject ON Course.Subject_ID = Subject.id;

-- Indexes for optimization
CREATE INDEX teacher_by_Name__IDX ON Teacher(first_name, last_name);
CREATE INDEX student_by_Name__IDX ON Student(first_name, last_name);
CREATE INDEX class_by_Name__IDX ON Class(name);

-- Procedure to change student’s class
DELIMITER //
CREATE PROCEDURE student_class_change(
    IN student_first_name VARCHAR(20),
    IN student_last_name VARCHAR(20),
    IN previous_class VARCHAR(10),
    IN new_class VARCHAR(10)
)
BEGIN
    DECLARE previous_class_id INT;
    DECLARE future_class_id INT;
    DECLARE highest_number INT;

    SELECT id INTO previous_class_id FROM Class WHERE name = previous_class;
    SELECT id INTO future_class_id FROM Class WHERE name = new_class;
    SELECT COALESCE(MAX(number_in_class_order), 0) + 1 INTO highest_number 
    FROM Student WHERE Class_ID = future_class_id;

    UPDATE Student 
    SET Class_ID = future_class_id, number_in_class_order = highest_number
    WHERE first_name = student_first_name 
    AND last_name = student_last_name 
    AND Class_ID = previous_class_id;
END //
DELIMITER ;

-- Procedure to list students in a specific course
DELIMITER //
CREATE PROCEDURE students_in_course(IN name_of_course VARCHAR(40))
BEGIN
    DECLARE id_of_course INT;
    SELECT id INTO id_of_course FROM Course WHERE course_name = name_of_course;

    SELECT first_name, last_name, number_in_class_order
    FROM Student
    WHERE Class_ID = id_of_course;
END //
DELIMITER ;

-- Procedure to list students in a specific class
DELIMITER //
CREATE PROCEDURE students_in_class(IN name_of_class VARCHAR(10), in in_grade int)
BEGIN
	DECLARE xclass_id INT;
	SELECT id INTO xclass_id FROM Class WHERE name = name_of_class and in_grade;
	
    SELECT first_name, last_name, number_in_class_order
    FROM Student
    WHERE (xclass_id = Class_ID AND is_student = 1);
END //
DELIMITER ;

-- Procedure to mark a student as inactive based on name and class
DELIMITER //
CREATE PROCEDURE set_previous_student_by_name(
    IN first_name_of_student VARCHAR(20),
    IN last_name_of_student VARCHAR(20),
    IN name_of_class VARCHAR(10)
)
BEGIN
    DECLARE class_id INT;
    DECLARE student_id INT;

    SELECT id INTO class_id FROM Class WHERE name = name_of_class AND active = 1;
    SELECT id INTO student_id FROM Student 
    WHERE first_name = first_name_of_student 
    AND last_name = last_name_of_student 
    AND Class_ID = class_id;

    UPDATE Student 
    SET is_student = 0
    WHERE id = student_id;
END //
DELIMITER ;

-- Procedure to mark all students in a class as inactive
DELIMITER //
CREATE PROCEDURE set_previous_students_by_class(IN name_of_class VARCHAR(10))
BEGIN
    DECLARE class_id INT;
    SELECT id INTO class_id FROM Class WHERE name = name_of_class AND active = 1;

    UPDATE Student
    SET is_student = 0
    WHERE Class_ID = class_id;
END //
DELIMITER ;

-- Procedure to assign a certificate to a teacher
DELIMITER //
CREATE PROCEDURE add_certificate_to_teacher(
    IN username_of_teacher VARCHAR(20),
    IN name_of_certificate VARCHAR(80),
    IN valide_since DATE
)
BEGIN
    DECLARE id_of_teacher INT;
    DECLARE id_of_certificate INT;

    SELECT id INTO id_of_teacher FROM Teacher WHERE teacher_username = username_of_teacher;
    SELECT id INTO id_of_certificate FROM Certificate WHERE certificate_name = name_of_certificate;

    INSERT INTO Own (valid_since, Ucitel_ID, Certifikat_ID) 
    VALUES (valide_since, id_of_teacher, id_of_certificate);
END //
DELIMITER ;

-- Trigger for inserting new students
DELIMITER //
CREATE TRIGGER Student_enroll
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    DECLARE highest_class_number INT;
    DECLARE same_name_count INT;
    SET highest_class_number = 1;

    SELECT COALESCE(MAX(number_in_class_order), 0) + 1 INTO highest_class_number
    FROM Student
    WHERE Class_ID = NEW.Class_ID;

    SELECT COUNT(*) INTO same_name_count
    FROM Student
    WHERE last_name = NEW.last_name;

    IF same_name_count = 0 THEN
        SET NEW.user_name = LOWER(NEW.last_name);
    ELSE
        SET NEW.user_name = LOWER(CONCAT(NEW.last_name, same_name_count));
    END IF;

    SET NEW.user_password = 'student';
    SET NEW.number_in_class_order = highest_class_number;
    SET NEW.is_student = 1;
END //
DELIMITER ;





INSERT INTO Teacher(first_name, last_name, teacher_username, teacher_password, email, phone_number) VALUES
('Jan', 'Švehl', 'svehl', 'repelent', 'svehl@gmail.com', '123456789'),
('Alena', 'Procházková', 'prochazkova', 'berusky', 'prochazkova@gmail.com', '147258369'),
('Karel', 'Hnízdo', 'hnizdo', 'modernebe', 'hnizdo@gmail.com', '159487263'),
('Přemek', 'Zahrádka', 'zahradka', 'lopatka', 'zahradka@gmail.com', '789632541'),
('Prokop', 'Novák', 'novak', 'dvere', 'novak@gmail.com', '753896412'),
('Zdeněk', 'Novák', 'novak1', 'zdenek', 'novak2@gmail.com', '968357241');

INSERT INTO Subject(subject_name, subject_description) VALUES
('Theoretical Computer Science', 'The science of how algorithms work'),
('Math', 'The science of the laws of mathematics'),
('Czech Language', 'Subject about correct use of Czech Language'),
('History', 'Subject on the history of the Czech kingdoms');

INSERT INTO Class(name,grade,number_of_class,year_of_entry,active,Class_Teacher_ID) VALUES 
('C1a', 1, 1, '2024-09-01', 1, 1),
('C1b', 1, 3, '2024-09-01', 1, 2),
('C2c', 2, 4, '2023-09-01', 1, 3),
('E3a', 3, 5, '2022-09-01', 1, 4),
('A4a', 4, 6, '2022-09-01', 1, 5),
('A4b', 4, 7, '2022-09-01', 1, 6);

INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('John', 'Smith', 1);
INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('Emma', 'Johnson', 2);
INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('Michael', 'Davis', 3);
INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('Sarah', 'Wilson', 4);
INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('David', 'Brown', 5);
INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('Lisa', 'Anderson', 6);
INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('James', 'Taylor', 3);
INSERT INTO Student(first_name,last_name,Class_ID) VALUES 
('Emily', 'Thomas', 1);

INSERT INTO student_card(town, street, descriptive_number, zip_code, email, date_of_birth, phone_number, Student_ID) VALUES
('Prague', 'Hlavni', '123/4', '12000', 'jan.novak@email.cz', '2009-03-15', '+420123456789', 1),
('Brno', 'Kolejni', '45/B', '60200', 'petra.svoboda@email.cz', '2009-08-22', '+420987654321', 2),
('Ostrava', 'Dlouha', '78/9', '70030', 'tomas.dvorak@email.cz', '2008-11-30', '+420456789123', 3),
('Plzen', 'Namesti', '456/12', '30100', 'lucie.nova@email.cz', '2007-05-17', '+420789123456', 4),
('Olomouc', 'Studentska', '321/7C', '77900', 'martin.kral@email.cz', '2006-02-28', '+420321654987', 5),
('Liberec', 'Technicka', '159/3', '46001', 'anna.vesela@email.cz', '2005-07-11', '+420147258369', 6),
('Hradec', 'Masarykova', '753/1', '50002', 'david.cerny@email.cz', '2008-12-04', '+420963852741', 7),
('Pardubice', 'Zelena', '852/9', '53002', 'eva.bila@email.cz', '2009-09-19', '+420741852963', 8);

INSERT INTO Certificate(certificate_name,issuing_organization,description) VALUES 
('AWS Certified Solutions Architect', 'Amazon Web Services', 'Professional certification for AWS cloud architecture and solutions'),
('Certified Information Systems Security Professional', 'ISC2', 'Advanced certification in information security and cybersecurity'),
('Microsoft Azure Administrator', 'Microsoft', 'Certification for implementing and managing Azure cloud environments'),
('CompTIA A+', 'CompTIA', 'Foundation certification for IT operational roles and computer hardware/software'),
('Certified Ethical Hacker', 'EC-Council', 'Professional certification in ethical hacking and penetration testing'),
('Cisco Certified Network Professional', 'Cisco', 'Advanced certification in enterprise networking solutions'),
('Project Management Professional', 'PMI', 'Certification for managing complex IT and software development projects'),
('Google Cloud Professional Architect', 'Google', 'Expert-level certification for Google Cloud Platform architecture');


INSERT INTO Course(course_name,number_of_theor_hours,number_of_practic_hours,Student_ID,Teacher_ID,Subject_ID) VALUES 
('TCS Fundamentals', 4, 2, 1, 1, 1),   
('TCS Advanced', 3, 3, 2, 1, 1),      
('TCS Practice', 2, 4, 3, 1, 1),       
('Mathematics 101', 4, 1, 4, 2, 2),     
('Advanced Algebra', 3, 2, 5, 2, 2),    
('Applied Mathematics', 2, 3, 6, 2, 2), 
('Czech Grammar', 3, 1, 7, 3, 3),       
('Czech Literature', 4, 0, 8, 3, 3),    
('Czech Writing', 2, 2, 1, 3, 3),      
('Czech History', 3, 0, 2, 4, 4),       
('Modern History', 3, 1, 4, 4, 4); 

INSERT INTO Grade(grade,description,date_of_award,Course_ID) VALUES 
(2, 'Midterm exam', '2024-03-15', 1),
(1, 'Final project', '2024-04-02', 1),
(3, 'Written test', '2024-03-10', 2),
(2, 'Practical exam', '2024-03-25', 2),
(1, 'Project presentation', '2024-03-20', 3),
(2, 'Code review', '2024-04-01', 3),
(4, 'Quiz results', '2024-03-12', 4),
(3, 'Homework assessment', '2024-03-28', 4),
(2, 'Written exam', '2024-03-18', 5),
(1, 'Group project', '2024-04-05', 5),
(3, 'Problem solving', '2024-03-22', 6),
(2, 'Final exam', '2024-04-08', 6),
(1, 'Essay writing', '2024-03-14', 7),
(2, 'Oral examination', '2024-03-30', 7),
(3, 'Book review', '2024-03-25', 8),
(2, 'Class participation', '2024-04-06', 8),
(1, 'Creative writing', '2024-03-19', 9),
(2, 'Grammar test', '2024-04-03', 9),
(2, 'History presentation', '2024-03-21', 10),
(3, 'Research paper', '2024-04-07', 11);

INSERT INTO  Own(valid_since, valid_to, Ucitel_ID, Certifikat_ID) Values
('2005-11-6', Null, 1, 1),
('2005-1-8', '2011-8-16', 2, 2),
('2006-8-7', Null, 3, 3),
('2012-8-16', '2016-7-12', 4, 4),
('2015-3-14', Null, 3, 5),
('2014-7-12', '2022-11-6', 5, 2),
('2019-7-14', '2027-8-7', 6, 8),
('2016-9-5', '2020-9-5', 2, 7);




