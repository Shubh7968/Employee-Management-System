create database employee;
use employee;

CREATE TABLE admins (
    admin_id VARCHAR(50) PRIMARY KEY,
	admin_pwd VARCHAR(255)
 );
 insert into admins values("myadmin@company.com","admin123");
 select * from admins;
 
create table employee(
	emp_id VARCHAR(50) PRIMARY KEY,
    emp_name VARCHAR(255),
    department VARCHAR(255),
	designation VARCHAR(255),
    salary DECIMAL(12,2)
);
ALTER TABLE employee ADD COLUMN emp_pwd VARCHAR(255) NOT NULL AFTER salary;
insert into employee values("E001","Shubham Chaudhary","IT Department","Data Analyst","37000.00");
UPDATE employee SET emp_pwd = 'mypassword123' WHERE emp_id = 'E001';
select * from employee;

CREATE TABLE attendance (
    emp_id VARCHAR(50),
    att_date DATE,
    status ENUM('Present','Absent','Leave') DEFAULT 'Present',
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
    PRIMARY KEY (emp_id, att_date)
 );
insert into attendance values("E001","2025-09-26","Leave");
select * from attendance;

create table request (
    emp_id VARCHAR(50),
    start_date DATE,
    end_date DATE,
    reason TEXT,
	status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
    primary key (emp_id, start_date, end_date) 
 );
insert into request values("E001","2025-09-26","2025-09-30","Fever","Approved");
select * from request; 

CREATE TABLE performance (
    emp_id VARCHAR(50),
    review_period VARCHAR(50),
    score INT,
    feedback TEXT,
    PRIMARY KEY(emp_id, review_period),
    FOREIGN KEY(emp_id) REFERENCES employee(emp_id)
);
INSERT INTO performance VALUES ('E001', '2025-Q3', 8, 'Good performance with timely project completion.');
select * from performance;

CREATE TABLE projects (
    project_id VARCHAR(50) PRIMARY KEY,
    project_name VARCHAR(255),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('Not Started', 'In Progress', 'Completed') DEFAULT 'Not Started'
);
insert into projects values ("P001",'Data Migration', 'Migrate all data from old CRM to new system.', '2025-07-01', '2025-09-30', 'Completed');
select * from projects;

CREATE TABLE project_assignments (
    emp_id VARCHAR(50),
    project_id VARCHAR(50),
    role VARCHAR(100),
    PRIMARY KEY(emp_id, project_id),
    FOREIGN KEY(emp_id) REFERENCES employee(emp_id),
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
insert into project_assignments values('E001', 'P001', 'Data Analyst');
select * from project_assignments;

