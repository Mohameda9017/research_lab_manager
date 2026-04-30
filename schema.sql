
-- since we are using SQLite and this command tells it to check for foreign key rules 
PRAGMA foreign_keys = ON;

-- allows us to rerun the schema without having to get errors 
DROP TABLE IF EXISTS PUBLISH;
DROP TABLE IF EXISTS IS_USED;
DROP TABLE IF EXISTS WORKS_ON;
DROP TABLE IF EXISTS GRANT_INFO;
DROP TABLE IF EXISTS PUBLICATION;
DROP TABLE IF EXISTS DEVICE;
DROP TABLE IF EXISTS EQUIPMENT;
DROP TABLE IF EXISTS PROJECT;
DROP TABLE IF EXISTS EXTERNAL_COLLABORATOR;
DROP TABLE IF EXISTS STUDENT;
DROP TABLE IF EXISTS FACULTY;
DROP TABLE IF EXISTS LAB_MEMBER;

CREATE TABLE LAB_MEMBER (
    Member_ID INT NOT NULL,
    Member_Name VARCHAR(30) NOT NULL,
    Join_Date DATE NOT NULL,
    Mentor_MID INT,
    Member_Type INT NOT NULL,
    Start_Mentorship_Date DATE,
    End_Mentorship_Date DATE,
    PRIMARY KEY (Member_ID),
    FOREIGN KEY (Mentor_MID) REFERENCES LAB_MEMBER(Member_ID),
    CHECK (Member_Type IN (1, 2, 3)),
    CHECK (Mentor_MID IS NULL OR Mentor_MID <> Member_ID)
);

CREATE TABLE FACULTY (
    Member_ID INT NOT NULL,
    Department VARCHAR(50) NOT NULL,
    PRIMARY KEY (Member_ID),
    FOREIGN KEY (Member_ID) REFERENCES LAB_MEMBER(Member_ID)
);

CREATE TABLE STUDENT (
    Member_ID INT NOT NULL,
    SID CHAR(10) NOT NULL,
    Academic_Level VARCHAR(20) NOT NULL,
    Major VARCHAR(50) NOT NULL,
    PRIMARY KEY (Member_ID),
    UNIQUE (SID),
    FOREIGN KEY (Member_ID) REFERENCES LAB_MEMBER(Member_ID)
);

CREATE TABLE EXTERNAL_COLLABORATOR (
    Member_ID INT NOT NULL,
    Institutional_Affiliation VARCHAR(50) NOT NULL,
    Short_Curriculum_Vitae VARCHAR(200) NOT NULL,
    PRIMARY KEY (Member_ID),
    FOREIGN KEY (Member_ID) REFERENCES LAB_MEMBER(Member_ID)
);

CREATE TABLE PROJECT (
    Project_ID INT NOT NULL,
    Title VARCHAR(50) NOT NULL,
    Start_Date DATE,
    End_Date DATE,
    Project_Duration INT,
    Project_Status VARCHAR(20) NOT NULL,
    Project_Lead INT NOT NULL,
    PRIMARY KEY (Project_ID),
    FOREIGN KEY (Project_Lead) REFERENCES FACULTY(Member_ID),
    CHECK (Project_Status IN ('active', 'completed', 'paused'))
);

CREATE TABLE WORKS_ON (
    Member_ID INT NOT NULL,
    Project_ID INT NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Hours INT DEFAULT 0,
    PRIMARY KEY (Member_ID, Project_ID),
    FOREIGN KEY (Member_ID) REFERENCES LAB_MEMBER(Member_ID),
    FOREIGN KEY (Project_ID) REFERENCES PROJECT(Project_ID)
);

CREATE TABLE EQUIPMENT (
    EID INT NOT NULL,
    Type VARCHAR(30) NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Manual VARCHAR(300) NOT NULL,
    PRIMARY KEY (EID)
);

CREATE TABLE DEVICE (
    EID INT NOT NULL,
    Device_ID INT NOT NULL,
    Status VARCHAR(20),
    Purchase_Date DATE,
    PRIMARY KEY (EID, Device_ID),
    FOREIGN KEY (EID) REFERENCES EQUIPMENT(EID),
    CHECK (Status IN ('available', 'in use', 'retired'))
);

CREATE TABLE IS_USED (
    EID INT NOT NULL,
    Device_ID INT NOT NULL,
    Member_ID INT NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE,
    Purpose VARCHAR(200),
    PRIMARY KEY (EID, Device_ID, Member_ID, Start_Date),
    FOREIGN KEY (EID, Device_ID) REFERENCES DEVICE(EID, Device_ID),
    FOREIGN KEY (Member_ID) REFERENCES LAB_MEMBER(Member_ID)
);

CREATE TABLE PUBLICATION (
    PubID INT NOT NULL,
    Venue VARCHAR(50),
    Title VARCHAR(50),
    Pub_Month INT,
    Pub_Year INT,
    DOI VARCHAR(100),
    PRIMARY KEY (PubID),
    UNIQUE (DOI),
    CHECK (Pub_Month BETWEEN 1 AND 12)
);

CREATE TABLE PUBLISH (
    Member_ID INT NOT NULL,
    PubID INT NOT NULL,
    PRIMARY KEY (Member_ID, PubID),
    FOREIGN KEY (Member_ID) REFERENCES LAB_MEMBER(Member_ID),
    FOREIGN KEY (PubID) REFERENCES PUBLICATION(PubID)
);

CREATE TABLE GRANT_INFO (
    Grant_ID INT NOT NULL,
    Budget INT,
    Start_Date DATE,
    Planned_Duration INT,
    Agency VARCHAR(50),
    Project_ID INT NOT NULL,
    PRIMARY KEY (Grant_ID),
    FOREIGN KEY (Project_ID) REFERENCES PROJECT(Project_ID)
);