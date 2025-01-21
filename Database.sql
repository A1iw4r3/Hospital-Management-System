CREATE DATABASE hys;
USE hys;

CREATE TABLE Employee (
    ID INT AUTO_INCREMENT PRIMARY KEY,  
    Name VARCHAR(255) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Phone_number VARCHAR(15) NOT NULL,
    Designation VARCHAR(255),
    Password VARCHAR(255) NOT NULL
);

-- Create Patient table
CREATE TABLE Patient (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY,  -- Change to INT
    Name VARCHAR(255) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Phone_number VARCHAR(15) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Create Bill table
CREATE TABLE Bill (
    Bill_ID INT AUTO_INCREMENT PRIMARY KEY,  -- Add a primary key for the Bill table
    Patient_ID INT,
    Bill DECIMAL(10, 2),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Create Medicine table
CREATE TABLE Medicine (
    Medicine_ID INT AUTO_INCREMENT PRIMARY KEY,  -- Add a primary key for the Medicine table
    Patient_ID INT,
    Medicines TEXT,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Create Report table
CREATE TABLE Report (
    Report_ID INT AUTO_INCREMENT PRIMARY KEY,  -- Add a primary key for the Report table
    Patient_ID INT,
    Reports TEXT,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID)
);

-- Insert random data into Employee table with MD5 hash of names
INSERT INTO Employee (Name, Gender, Email, Phone_number, Designation, Password)
VALUES
    ('John Doe', 'Male', 'john.doe@example.com', '1234567890', 'Doctor', MD5('John Doe')),
    ('Alice Smith', 'Female', 'alice.smith@example.com', '0987654321', 'Nurse', MD5('Alice Smith')),
    ('Michael Brown', 'Male', 'michael.brown@example.com', '1122334455', 'Receptionist', MD5('Michael Brown')),
    ('Emma Johnson', 'Female', 'emma.johnson@example.com', '2233445566', 'Administrator', MD5('Emma Johnson')),
    ('Daniel Lee', 'Male', 'daniel.lee@example.com', '3344556677', 'Surgeon', MD5('Daniel Lee'));

-- Insert random data into Patient table with MD5 hash of names
INSERT INTO Patient (Name, Gender, Email, Phone_number, Password)
VALUES
    ('Olivia Williams', 'Female', 'olivia.williams@example.com', '4455667788', MD5('Olivia Williams')),
    ('Liam Wilson', 'Male', 'liam.wilson@example.com', '5566778899', MD5('Liam Wilson')),
    ('Sophia Martinez', 'Female', 'sophia.martinez@example.com', '6677889900', MD5('Sophia Martinez')),
    ('Noah Anderson', 'Male', 'noah.anderson@example.com', '7788990011', MD5('Noah Anderson')),
    ('Mia Thomas', 'Female', 'mia.thomas@example.com', '8899001122', MD5('Mia Thomas'));

-- Insert random data into Bill table
INSERT INTO Bill (Patient_ID, Bill)
VALUES
    (1, 150.75),
    (2, 200.50),
    (3, 120.30),
    (4, 300.00),
    (5, 180.25);

-- Insert random data into Medicine table
INSERT INTO Medicine (Patient_ID, Medicines)
VALUES
    (1, 'Paracetamol, Ibuprofen'),
    (2, 'Amoxicillin, Cough Syrup'),
    (3, 'Aspirin, Vitamin C'),
    (4, 'Insulin, Blood Pressure Medicine'),
    (5, 'Pain Relief, Antibiotics');

-- Insert random data into Report table
INSERT INTO Report (Patient_ID, Reports)
VALUES
    (1, 'Blood Test: Normal, X-Ray: Clear'),
    (2, 'CT Scan: Mild Infection'),
    (3, 'MRI: No Issues'),
    (4, 'Blood Pressure Report: High, Diabetes Check: Positive'),
    (5, 'X-Ray: No Issues, Blood Test: Normal');

ALTER TABLE Employee
  MODIFY id INT PRIMARY KEY;
ALTER TABLE Patient
  MODIFY id INT PRIMARY KEY;
-- 
describe employee;
select * from employee;