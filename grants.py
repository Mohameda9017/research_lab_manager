import sqlite3

DB_NAME = "lab.db"

def connect():
    """Connects Python to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def top5projectsbygrant():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            P.Project_ID,
            P.Title,
            COALESCE(SUM(G.Budget), 0) AS Total_Funding
        FROM PROJECT AS P
        LEFT JOIN GRANT_INFO AS G
            ON P.Project_ID = G.Project_ID
        GROUP BY P.Project_ID, P.Title
        ORDER BY Total_Funding DESC
        LIMIT 5;
    """)

    results = cursor.fetchall()

    if results:
        print("\n--- Top 5 Projects by Total Grant Funding ---")
        for row in results:
            print(
                f"Project ID: {row[0]} | "
                f"Project: {row[1]} | "
                f"Total Funding: ${row[2]}"
            )
    else:
        print("No projects found.")

    conn.close()

def mentormostpublication():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        WITH MentorPublicationCounts AS (
            SELECT
                Mentor.Member_ID AS Mentor_ID,
                Mentor.Member_Name AS Mentor_Name,
                COUNT(DISTINCT Pub.PubID) AS Publication_Count
            FROM LAB_MEMBER AS Mentee
            JOIN LAB_MEMBER AS Mentor
                ON Mentee.Mentor_MID = Mentor.Member_ID
            JOIN PUBLISH AS Pub
                ON Mentee.Member_ID = Pub.Member_ID
            GROUP BY Mentor.Member_ID, Mentor.Member_Name
        )
        SELECT Mentor_ID, Mentor_Name, Publication_Count
        FROM MentorPublicationCounts
        WHERE Publication_Count = (
            SELECT MAX(Publication_Count)
            FROM MentorPublicationCounts
        );
    """)

    results = cursor.fetchall()

    if results:
        print("\n--- Mentor(s) Whose Mentees Produced the Most Publications ---")
        for row in results:
            print(
                f"Mentor ID: {row[0]} | "
                f"Mentor Name: {row[1]} | "
                f"Publication Count: {row[2]}"
            )
    else:
        print("No mentor publication data found.")

    conn.close()

def student_publications_by_major_and_year():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            S.Major,
            Pub.Pub_Year,
            COUNT(DISTINCT Pub.PubID) AS Publication_Count
        FROM STUDENT AS S
        JOIN PUBLISH AS P
            ON S.Member_ID = P.Member_ID
        JOIN PUBLICATION AS Pub
            ON P.PubID = Pub.PubID
        GROUP BY S.Major, Pub.Pub_Year
        ORDER BY Pub.Pub_Year, S.Major;
    """)

    results = cursor.fetchall()

    if results:
        print("\n--- Student Publications Per Major and Publication Year ---")
        for row in results:
            print(
                f"Major: {row[0]} | "
                f"Year: {row[1]} | "
                f"Publication Count: {row[2]}"
            )
    else:
        print("No student publication data found.")

    conn.close()

def projects_ended_before_date():
    conn = connect()
    cursor = conn.cursor()

    date_x = input("Enter date X (YYYY-MM-DD): ")

    cursor.execute("""
        SELECT
            P.Project_ID,
            P.Title,
            P.End_Date,
            COUNT(G.Grant_ID) AS Grant_Count
        FROM PROJECT AS P
        LEFT JOIN GRANT_INFO AS G
            ON P.Project_ID = G.Project_ID
        WHERE P.End_Date IS NOT NULL
          AND P.End_Date < ?
        GROUP BY P.Project_ID, P.Title, P.End_Date
        ORDER BY P.End_Date;
    """, (date_x,))

    results = cursor.fetchall()

    if results:
        print(f"\n--- Projects Ended Before {date_x} and Number of Grants ---")
        for row in results:
            print(
                f"Project ID: {row[0]} | "
                f"Title: {row[1]} | "
                f"End Date: {row[2]} | "
                f"Number of Grants: {row[3]}"
            )
    else:
        print("No projects found before that date.")

    conn.close()

def threemostprodpubyear():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Pub.Pub_Year,
            COUNT(DISTINCT Pub.PubID) AS Publication_Count
        FROM STUDENT AS S
        JOIN PUBLISH AS P
            ON S.Member_ID = P.Member_ID
        JOIN PUBLICATION AS Pub
            ON P.PubID = Pub.PubID
        GROUP BY Pub.Pub_Year
        ORDER BY Publication_Count DESC
        LIMIT 3;
    """)

    results = cursor.fetchall()

    if results:
        print("\n--- Top 3 Productive Years for Student Publications ---")
        for row in results:
            print(
                f"Year: {row[0]} | "
                f"Student Publication Count: {row[1]}"
            )
    else:
        print("No student publication data found.")

    conn.close()

def grantpublication_reporting_menu():
    while True:
        print("\n--- Grant and Publication Reporting ---")
        print("1. List top 5 projects by total grant funding")
        print("2. Find mentor(s) whose mentees produced the most publications")
        print("3. Calculate student publications per major and publication year")
        print("4. Find projects ended before date X and number of grants")
        print("5. Find top 3 productive years for student publications")
        print("6. Back to main menu")

        choice = input("Choose an Option: ")

        if choice == "1":
            top5projectsbygrant()
        elif choice == "2":
            mentormostpublication()
        elif choice == "3":
            student_publications_by_major_and_year()
        elif choice == "4":
            projects_ended_before_date()
        elif choice == "5":
            threemostprodpubyear()
        elif choice == "6":
            break
        else:
            print("Enter a valid choice.")
