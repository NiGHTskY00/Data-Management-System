-- Create the database
CREATE DATABASE TrainingProgramDB;

-- Use the database
USE TrainingProgramDB;

-- Create Students Table
CREATE TABLE Students (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(50),
    Gender VARCHAR(10), -- Male/Female
    Grade INT CHECK (Grade BETWEEN 6 AND 12),
    Date_Of_Joining DATE,
    Mail_ID VARCHAR(100),
    Parent_Phone_No VARCHAR(15),
    Active_Status BOOLEAN -- 1 for active, 0 for inactive
);

-- Create Trainers Table
CREATE TABLE Trainers (
    Trainer_ID INT PRIMARY KEY,
    Name VARCHAR(50),
    Expertise VARCHAR(50),
    Class_Grade INT CHECK (Class_Grade BETWEEN 6 AND 12),
    Specialization VARCHAR(100)
);

-- Create Subjects Table
CREATE TABLE Subjects (
    Subject_ID INT PRIMARY KEY,
    Subject_Name VARCHAR(50),
    Subject_Description TEXT
);

-- Create Attendance Table
CREATE TABLE Attendance (
    Attendance_ID INT PRIMARY KEY,
    Student_ID INT,
    Trainer_ID INT,
    Subject_ID INT,
    Date DATE,
    Attendance_Status VARCHAR(10), -- Present/Absent
    Engagement_Impact FLOAT, -- Optional, for tracking engagement
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID),
    FOREIGN KEY (Trainer_ID) REFERENCES Trainers(Trainer_ID),
    FOREIGN KEY (Subject_ID) REFERENCES Subjects(Subject_ID)
);

-- Create Student Performance Table
CREATE TABLE Student_Performance (
    Performance_ID INT PRIMARY KEY,
    Student_ID INT,
    Week_Number INT CHECK (Week_Number BETWEEN 1 AND 16), -- 4 months = 16 weeks
    Engagement_Score INT CHECK (Engagement_Score BETWEEN 1 AND 5),
    Task_Status VARCHAR(20), -- Completed/Incomplete
    Custom_Performance_Index FLOAT,
    Feedback TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

-- Create Material Usage Table
CREATE TABLE Material_Usage (
    Material_ID INT PRIMARY KEY,
    Student_ID INT,
    Material_Type VARCHAR(50),
    Usage_Percentage FLOAT CHECK (Usage_Percentage BETWEEN 0 AND 100),
    Effectiveness_Score FLOAT,
    Feedback_m TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

-- Create Method Effectiveness Table
CREATE TABLE Method_Effectiveness (
    Method_Effectiveness_ID INT PRIMARY KEY,
    Trainer_ID INT,
    Engagement_Score FLOAT CHECK (Engagement_Score BETWEEN 1 AND 5),
    Course_Completion_Percentage FLOAT CHECK (Course_Completion_Percentage BETWEEN 0 AND 100),
    Student_Feedback_Rating FLOAT CHECK (Student_Feedback_Rating BETWEEN 1 AND 5),
    Date_Feedback_Provided DATE,
    Method_Description TEXT,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainers(Trainer_ID)
);

-- Create Assessments Table
CREATE TABLE Assessments (
    Assessment_ID INT PRIMARY KEY,
    Student_ID INT,
    Type VARCHAR(10) CHECK (Type IN ('Baseline', 'Endline')),
    Score FLOAT,
    Feedback_a TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

