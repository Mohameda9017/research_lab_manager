PRAGMA foreign_keys = ON;

-- this clears the old data inside these tables so we can rerun it. 
DELETE FROM PUBLISH;
DELETE FROM IS_USED;
DELETE FROM WORKS_ON;
DELETE FROM GRANT_INFO;
DELETE FROM PUBLICATION;
DELETE FROM DEVICE;
DELETE FROM EQUIPMENT;
DELETE FROM PROJECT;
DELETE FROM EXTERNAL_COLLABORATOR;
DELETE FROM STUDENT;
DELETE FROM FACULTY;
-- Since LAB_MEMBER has a self foreign key for Mentor_MID, we first remove mentor references before deleting members.
UPDATE LAB_MEMBER SET Mentor_MID = NULL;
DELETE FROM LAB_MEMBER;


-- Member_Type meanings:
-- 1 = Student
-- 2 = Faculty
-- 3 = External Collaborator

INSERT INTO LAB_MEMBER
(Member_ID,Member_Name,Join_Date, Mentor_MID, Member_Type, Start_Mentorship_Date, End_Mentorship_Date) VALUES
(101,'Dr. Sarah Kim','2020-08-15',NULL, 2, NULL, NULL),
(102,'Dr. James Wilson','2019-01-10', NULL, 2, NULL, NULL),
(103,'Dr. Maria Garcia','2021-06-01',NULL, 2, NULL, NULL),
(201,'Alex Chen','2023-09-01', 101,1, '2023-09-15', NULL),
(202,'Priya Patel','2022-09-01', 101, 1, '2022-09-20', NULL),
(203,'Omar Hassan','2024-01-15', 102, 1, '2024-02-01', NULL),
(204,'Emily Davis', '2023-01-20', 102, 1,'2023-02-01', NULL),
(205,'Daniel Lee','2022-06-10',103, 1, '2022-07-01', NULL),
(206,'Sophia Martinez','2024-09-01',103,1,'2024-09-10', NULL),
(207,'Noah Brown', '2023-05-05', 101, 1, '2023-05-20', NULL),
(208, 'Maya Johnson','2022-11-12', 102, 1, '2022-12-01', NULL),
(301,'Dr. Robert Evans', '2021-03-12', 103, 3,'2021-04-01', NULL),
(302,'Dr. Linda Park', '2022-07-18', 101, 3,'2022-08-01', NULL),
(303,'Dr. Kevin Moore', '2023-10-05', 102, 3, '2023-10-20', NULL);


INSERT INTO FACULTY
(Member_ID, Department) VALUES
(101, 'Computer Science'),
(102, 'Electrical Engineering'),
(103, 'Data Science');


INSERT INTO STUDENT
(Member_ID, SID, Academic_Level, Major)
VALUES
(201, '1000000001', 'Graduate', 'Computer Science'),
(202, '1000000002', 'Graduate', 'Data Science'),
(203, '1000000003', 'Senior', 'Computer Science'),
(204, '1000000004', 'Junior', 'Information Systems'),
(205, '1000000005', 'Graduate', 'Computer Science'),
(206, '1000000006', 'Senior', 'Data Science'),
(207, '1000000007', 'Junior', 'Computer Engineering'),
(208, '1000000008', 'Graduate', 'Information Systems');


INSERT INTO EXTERNAL_COLLABORATOR
(Member_ID, Institutional_Affiliation, Short_Curriculum_Vitae) VALUES
(301, 'Princeton University', 'Researcher in machine learning and scientific computing.'),
(302, 'Rutgers University', 'Collaborator specializing in database systems and data modeling.'),
(303, 'Stevens Institute of Technology', 'Research scientist focused on sensor systems and robotics.');


INSERT INTO PROJECT
(Project_ID, Title, Start_Date, End_Date, Project_Duration, Project_Status, Project_Lead)
VALUES
(401, 'Wildfire Spread Prediction', '2023-09-01', NULL, 24, 'active', 101),
(402, 'Smart Lab Sensor Network', '2022-06-01', '2024-06-01', 24, 'completed', 102),
(403, 'Medical Image Classification', '2024-01-15', NULL, 18, 'active', 103),
(404, 'Database Automation System', '2021-09-01', '2023-12-15', 27, 'completed', 101),
(405, 'Robotics Vision Platform', '2023-03-10', NULL, 30, 'paused', 102),
(406, 'Climate Data Integration', '2022-01-20', '2024-01-20', 24, 'completed', 103),
(407, 'AI Research Assistant', '2024-08-01', NULL, 12, 'active', 101);


INSERT INTO WORKS_ON
(Member_ID, Project_ID, Role, Hours)
VALUES
(101, 401, 'Project Lead', 8),
(201, 401, 'ML Developer', 12),
(202, 401, 'Data Analyst', 10),
(207, 401, 'Research Assistant', 6),
(301, 401, 'External Advisor', 4),
(102, 402, 'Project Lead', 7),
(203, 402, 'Sensor Programmer', 10),
(204, 402, 'Database Assistant', 8),
(303, 402, 'Robotics Consultant', 5),
(103, 403, 'Project Lead', 9),
(205, 403, 'Model Developer', 12),
(206, 403, 'Data Preprocessing Assistant', 8),
(302, 403, 'Research Collaborator', 5),
(101, 404, 'Project Lead', 6),
(202, 404, 'Database Designer', 9),
(204, 404, 'Backend Developer', 10),
(208, 404, 'Report Developer', 7),
(102, 405, 'Project Lead', 8),
(203, 405, 'Computer Vision Assistant', 9),
(207, 405, 'Testing Assistant', 6),
(303, 405, 'Robotics Advisor', 5),
(103, 406, 'Project Lead', 7),
(205, 406, 'Data Engineer', 10),
(206, 406, 'Visualization Assistant', 6),
(301, 406, 'Scientific Computing Advisor', 4),
(101, 407, 'Project Lead', 8),
(201, 407, 'LLM Developer', 11),
(208, 407, 'Evaluation Assistant', 7),
(302, 407, 'Database Advisor', 4);

INSERT INTO GRANT_INFO
(Grant_ID, Budget, Start_Date, Planned_Duration, Agency, Project_ID)
VALUES
(501, 150000, '2023-09-01', 24, 'NSF', 401),
(502, 75000, '2024-01-01', 12, 'NJIT Research Office', 401),
(503, 120000, '2022-06-01', 24, 'DARPA', 402),
(504, 200000, '2024-02-01', 18, 'NIH', 403),
(505, 50000, '2024-06-01', 12, 'HealthTech Foundation', 403),
(506, 90000, '2021-09-01', 24, 'NSF', 404),
(507, 60000, '2023-03-10', 18, 'Robotics Institute', 405),
(508, 110000, '2022-01-20', 24, 'NOAA', 406),
(509, 175000, '2024-08-01', 12, 'OpenAI Academic Research Fund', 407),
(510, 40000, '2024-10-01', 10, 'NJIT Innovation Fund', 407);


INSERT INTO EQUIPMENT
(EID, Type, Name, Manual)
VALUES
(601, 'GPU Server', 'NVIDIA Research Server', 'Manual for server access, GPU scheduling, and safety rules.'),
(602, 'Microscope', 'Digital Lab Microscope', 'Manual for microscope calibration and image capture.'),
(603, 'Sensor Kit', 'Environmental Sensor Kit', 'Manual for temperature, humidity, and air-quality sensor setup.'),
(604, '3D Printer', 'Lab 3D Printer', 'Manual for printing, filament loading, and maintenance.'),
(605, 'Robot Platform', 'Autonomous Robot Platform', 'Manual for robot charging, calibration, and movement testing.');


INSERT INTO DEVICE
(EID, Device_ID, Status, Purchase_Date)
VALUES
(601, 1, 'in use', '2022-08-01'),
(601, 2, 'available', '2023-01-15'),
(602, 1, 'available', '2021-05-20'),
(602, 2, 'retired', '2018-09-10'),
(603, 1, 'in use', '2022-11-05'),
(603, 2, 'available', '2023-04-22'),
(604, 1, 'in use', '2020-07-18'),
(604, 2, 'available', '2022-02-12'),
(605, 1, 'in use', '2023-03-01'),
(605, 2, 'available', '2024-01-25');



INSERT INTO IS_USED
(EID, Device_ID, Member_ID, Start_Date, End_Date, Purpose)
VALUES
(601, 1, 201, '2024-09-01', NULL, 'Training wildfire prediction models'),
(601, 1, 202, '2024-09-05', NULL, 'Running data preprocessing experiments'),
(601, 1, 207, '2024-09-10', NULL, 'Testing model evaluation scripts'),

(601, 2, 205, '2024-02-01', '2024-04-01', 'Training medical image models'),

(603, 1, 203, '2024-03-15', NULL, 'Collecting smart lab sensor readings'),
(603, 1, 204, '2024-03-20', NULL, 'Testing database logging for sensor data'),

(604, 1, 205, '2024-05-01', NULL, 'Printing medical device prototype parts'),
(604, 1, 206, '2024-05-10', NULL, 'Testing prototype casing designs'),

(605, 1, 203, '2024-08-01', NULL, 'Testing robot vision movement'),
(605, 1, 303, '2024-08-05', NULL, 'Robotics platform calibration'),

(602, 1, 206, '2024-01-10', '2024-02-10', 'Capturing image samples for classification'),
(602, 1, 302, '2024-02-15', '2024-03-01', 'Reviewing image quality for publication.');

INSERT INTO PUBLICATION
(PubID, Venue, Title, Pub_Month, Pub_Year, DOI)
VALUES
(701, 'IEEE Big Data', 'Wildfire Spread Prediction Using CNNs', 11, 2024, '10.1000/wildfire001'),
(702, 'ACM SIGMOD Workshop', 'Automating Research Lab Databases', 6, 2023, '10.1000/database002'),
(703, 'Sensors Journal', 'Smart Lab Sensor Network Design', 9, 2023, '10.1000/sensor003'),
(704, 'Medical Imaging Conference', 'Deep Learning for Medical Image Classification', 3, 2025, '10.1000/medical004'),
(705, 'Robotics Symposium', 'Vision-Based Navigation for Lab Robots', 7, 2024, '10.1000/robot005'),
(706, 'Climate Informatics', 'Integrating Climate Data for Research Labs', 5, 2024, '10.1000/climate006'),
(707, 'AI Systems Conference', 'Building an AI Research Assistant', 10, 2025, '10.1000/ai007'),
(708, 'Data Science Review', 'Evaluation Metrics for Imbalanced Spatial Prediction', 12, 2024, '10.1000/metrics008'),
(709, 'University Research Journal', 'Database Support for Research Lab Management', 4, 2022, '10.1000/labdb009'),
(710, 'Machine Learning Applications', 'Threshold Tuning in Fire Spread Prediction', 2, 2025, '10.1000/threshold010');


INSERT INTO PUBLISH
(Member_ID, PubID)
VALUES
(101, 701),
(201, 701),
(202, 701),
(301, 701),

(101, 702),
(202, 702),
(204, 702),
(302, 702),

(102, 703),
(203, 703),
(204, 703),
(303, 703),

(103, 704),
(205, 704),
(206, 704),
(302, 704),

(102, 705),
(203, 705),
(207, 705),
(303, 705),

(103, 706),
(205, 706),
(206, 706),
(301, 706),

(101, 707),
(201, 707),
(208, 707),
(302, 707),

(101, 708),
(201, 708),
(202, 708),
(207, 708),

(101, 709),
(204, 709),
(208, 709),

(101, 710),
(201, 710),
(202, 710),
(301, 710);.