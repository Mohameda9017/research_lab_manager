import sqlite3
from grants import grantpublication_reporting_menu
from equipment import equipment_menu


# helper function to take in any enters as just null values 
def blank_to_none(value):
    value = value.strip()
    if value == "":
        return None
    return value

DB_NAME = "lab.db"

def connect():
    """Connects Python to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def query_all_members():
    ''' querys all the members from the lab memebers table and prints them'''
    conn = connect()

    cursor = conn.cursor() # the cursor object is that one that runs the SQL commands 
    cursor.execute("""
        SELECT Member_ID, Member_Name, Join_Date, Member_Type
        FROM LAB_MEMBER; """)
    
    results = cursor.fetchall() # this gets all the results from the query. stored in a list of tuples, where each tuple is a result. 

    print("\n--- All Lab Members ---")
    for row in results: 
        print(f"ID: {row[0]} | Name: {row[1]} | Join Date: {row[2]} | Type: {row[3]}")

    conn.close() # closes the connecttion with the database
    
def display_project_status():
    conn = connect()
    cursor = conn.cursor()
    project_id = input("Enter Project ID: ")
    cursor.execute("""SELECT Project_ID, Title, Project_Status
                   FROM PROJECT
                   WHERE Project_ID = ? 
                   """, (project_id,)) # note the ? stands for a placeholder which will we specifcy as a second argument

    result = cursor.fetchone()

    if result: 
        print("\n--- Project Status ---")
        print(f'Project ID {result[0]}')
        print(f'Project Title {result[1]}')
        print(f'Project Status {result[2]}')
    else:
        print("No project found with that ID.")
    
    conn.close()

def query_all_projects():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
                SELECT * 
                   FROM PROJECT
                   """)
    results = cursor.fetchall()
    for row in results:
        print(
            f"ID: {row[0]} | Title: {row[1]} | Start: {row[2]} | "
            f"End: {row[3]} | Duration: {row[4]} months | "
            f"Status: {row[5]} | Lead ID: {row[6]}"
        )
    
    conn.close()

def show_members_by_grant():
    
    conn = connect()
    cursor = conn.cursor()
    grant_id = input("Enter Grant ID: ")

    cursor.execute("""
        SELECT L.Member_ID,L.Member_Name,P.Title,W.Role,W.Hours
        FROM GRANT_INFO AS G
        JOIN PROJECT AS P
            ON G.Project_ID = P.Project_ID
        JOIN WORKS_ON AS W
            ON P.Project_ID = W.Project_ID
        JOIN LAB_MEMBER AS L
            ON W.Member_ID = L.Member_ID
        WHERE G.Grant_ID = ?;
    """, (grant_id,))
    results = cursor.fetchall()

    if results:
        print("\n--- Members Who Worked on Projects Funded by This Grant ---")
        for row in results:
            print(
                f"Member ID: {row[0]} | "
                f"Name: {row[1]} | "
                f"Project: {row[2]} | "
                f"Role: {row[3]} | "
                f"Hours: {row[4]}"
            )
    else:
        print("No members found for that grant ID.")
    
    conn.close()

def show_mentorships_same_project():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            P.Project_ID,
            P.Title,
            M.Member_Name AS Mentor_Name,
            L.Member_Name AS Mentee_Name,
            L.Start_Mentorship_Date,
            L.End_Mentorship_Date
        FROM LAB_MEMBER AS L
        JOIN LAB_MEMBER AS M
            ON L.Mentor_MID = M.Member_ID
        JOIN WORKS_ON AS W1
            ON L.Member_ID = W1.Member_ID
        JOIN WORKS_ON AS W2
            ON M.Member_ID = W2.Member_ID
            AND W1.Project_ID = W2.Project_ID
        JOIN PROJECT AS P
            ON W1.Project_ID = P.Project_ID
        WHERE L.Mentor_MID IS NOT NULL;
    """)
    results = cursor.fetchall()

    if results:
        print("\n--- Mentorship Relations Among Members on the Same Project ---")
        for row in results:
            print(
                f"Project ID: {row[0]} | "
                f"Project: {row[1]} | "
                f"Mentor: {row[2]} | "
                f"Mentee: {row[3]} | "
                f"Start: {row[4]} | "
                f"End: {row[5]}"
            )
    else:
        print("No mentorship relations found among members on the same project.")

    conn.close()

def add_member():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Add Member ---")
    print("Member Type: 1 = Student, 2 = Faculty, 3 = External Collaborator")

    member_id = input("Enter Member ID: ")
    member_name = input("Enter Member Name: ")
    join_date = input("Enter Join Date (YYYY-MM-DD): ")
    mentor_mid = blank_to_none(input("Enter Mentor ID or press Enter for none: "))
    member_type = input("Enter Member Type: ")
    start_mentorship_date = blank_to_none(input("Enter Mentorship Start Date or press Enter for none: "))
    end_mentorship_date = blank_to_none(input("Enter Mentorship End Date or press Enter for none: "))

    try:
        cursor.execute("""
            INSERT INTO LAB_MEMBER
            (Member_ID, Member_Name, Join_Date, Mentor_MID, Member_Type, Start_Mentorship_Date, End_Mentorship_Date)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            member_id,
            member_name,
            join_date,
            mentor_mid,
            member_type,
            start_mentorship_date,
            end_mentorship_date
        ))

        if member_type == "1":
            sid = input("Enter Student ID: ")
            academic_level = input("Enter Academic Level: ")
            major = input("Enter Major: ")

            cursor.execute("""
                INSERT INTO STUDENT
                (Member_ID, SID, Academic_Level, Major)
                VALUES (?, ?, ?, ?);
            """, (member_id, sid, academic_level, major))

        elif member_type == "2":
            department = input("Enter Department: ")

            cursor.execute("""
                INSERT INTO FACULTY
                (Member_ID, Department)
                VALUES (?, ?);
            """, (member_id, department))

        elif member_type == "3":
            affiliation = input("Enter Institutional Affiliation: ")
            cv = input("Enter Short Curriculum Vitae: ")

            cursor.execute("""
                INSERT INTO EXTERNAL_COLLABORATOR
                (Member_ID, Institutional_Affiliation, Short_Curriculum_Vitae)
                VALUES (?, ?, ?);
            """, (member_id, affiliation, cv))

        else:
            print("Invalid member type. Member was not added.")
            conn.rollback()
            return

        conn.commit()
        print("Member added successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error adding member:", e)

    finally:
        conn.close()

def update_member():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Update Member ---")
    member_id = input("Enter Member ID to update: ")

    cursor.execute("""
        SELECT Member_ID, Member_Name, Join_Date, Mentor_MID,
               Member_Type, Start_Mentorship_Date, End_Mentorship_Date
        FROM LAB_MEMBER
        WHERE Member_ID = ?;
    """, (member_id,))

    member = cursor.fetchone()

    if not member:
        print("No member found with that ID.")
        conn.close()
        return

    print("\nPress Enter to keep the current value.")

    new_name = input(f"Enter new name [{member[1]}]: ")
    new_join_date = input(f"Enter new join date [{member[2]}]: ")
    new_mentor = input(f"Enter new mentor ID [{member[3]}]: ")
    new_start = input(f"Enter new mentorship start date [{member[5]}]: ")
    new_end = input(f"Enter new mentorship end date [{member[6]}]: ")

    new_name = member[1] if new_name.strip() == "" else new_name
    new_join_date = member[2] if new_join_date.strip() == "" else new_join_date
    new_mentor = member[3] if new_mentor.strip() == "" else blank_to_none(new_mentor)
    new_start = member[5] if new_start.strip() == "" else blank_to_none(new_start)
    new_end = member[6] if new_end.strip() == "" else blank_to_none(new_end)

    try:
        cursor.execute("""
            UPDATE LAB_MEMBER
            SET Member_Name = ?,
                Join_Date = ?,
                Mentor_MID = ?,
                Start_Mentorship_Date = ?,
                End_Mentorship_Date = ?
            WHERE Member_ID = ?;
        """, (
            new_name,
            new_join_date,
            new_mentor,
            new_start,
            new_end,
            member_id
        ))

        conn.commit()
        print("Member updated successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error updating member:", e)

    conn.close()

def remove_member():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Remove Member ---")
    member_id = input("Enter Member ID to remove: ")

    cursor.execute("""
        SELECT Member_Name, Member_Type
        FROM LAB_MEMBER
        WHERE Member_ID = ?;
    """, (member_id,))

    member = cursor.fetchone()

    if not member:
        print("No member found with that ID.")
        conn.close()
        return

    # Do not remove a faculty member if they lead a project.
    cursor.execute("""
        SELECT Project_ID, Title
        FROM PROJECT
        WHERE Project_Lead = ?;
    """, (member_id,))

    led_projects = cursor.fetchall()

    if led_projects:
        print("Cannot remove this member because they lead project(s):")
        for row in led_projects:
            print(f"Project ID: {row[0]} | Title: {row[1]}")
        print("Update/remove those projects first.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to remove {member[0]}? (y/n): ")

    if confirm.lower() != "y":
        print("Remove canceled.")
        conn.close()
        return

    try:
        # If this member is someone else's mentor, remove that mentor reference first.
        cursor.execute("""
            UPDATE LAB_MEMBER
            SET Mentor_MID = NULL,
                Start_Mentorship_Date = NULL,
                End_Mentorship_Date = NULL
            WHERE Mentor_MID = ?;
        """, (member_id,))

        # Delete relationship rows first.
        cursor.execute("DELETE FROM WORKS_ON WHERE Member_ID = ?;", (member_id,))
        cursor.execute("DELETE FROM IS_USED WHERE Member_ID = ?;", (member_id,))
        cursor.execute("DELETE FROM PUBLISH WHERE Member_ID = ?;", (member_id,))

        # Delete from subtype table.
        if member[1] == 1:
            cursor.execute("DELETE FROM STUDENT WHERE Member_ID = ?;", (member_id,))
        elif member[1] == 2:
            cursor.execute("DELETE FROM FACULTY WHERE Member_ID = ?;", (member_id,))
        elif member[1] == 3:
            cursor.execute("DELETE FROM EXTERNAL_COLLABORATOR WHERE Member_ID = ?;", (member_id,))

        # Delete from main table.
        cursor.execute("DELETE FROM LAB_MEMBER WHERE Member_ID = ?;", (member_id,))

        conn.commit()
        print("Member removed successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error removing member:", e)

    conn.close()

def add_project():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Add Project ---")

    project_id = input("Enter Project ID: ")
    title = input("Enter Project Title: ")
    start_date = blank_to_none(input("Enter Start Date (YYYY-MM-DD): "))
    end_date = blank_to_none(input("Enter End Date or press Enter for none: "))
    duration = input("Enter Project Duration in months: ")
    status = input("Enter Project Status (active, completed, paused): ")
    project_lead = input("Enter Faculty Member ID as Project Lead: ")

    try:
        cursor.execute("""
            INSERT INTO PROJECT
            (Project_ID, Title, Start_Date, End_Date, Project_Duration, Project_Status, Project_Lead)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (project_id, title, start_date, end_date, duration, status, project_lead))

        conn.commit()
        print("Project added successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error adding project:", e)

    conn.close()


def update_project_status():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Update Project Status ---")
    project_id = input("Enter Project ID to update: ")
    new_status = input("Enter new status (active, completed, paused): ")

    cursor.execute("""
        UPDATE PROJECT
        SET Project_Status = ?
        WHERE Project_ID = ?;
    """, (new_status, project_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("Project status updated successfully.")
    else:
        print("No project found with that ID.")

    conn.close()


def remove_project():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Remove Project ---")
    project_id = input("Enter Project ID to remove: ")

    cursor.execute("""
        SELECT Title
        FROM PROJECT
        WHERE Project_ID = ?;
    """, (project_id,))

    project = cursor.fetchone()

    if not project:
        print("No project found with that ID.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to remove project '{project[0]}'? (y/n): ")

    if confirm.lower() != "y":
        print("Remove canceled.")
        conn.close()
        return

    try:
        # Delete rows that depend on this project first.
        cursor.execute("DELETE FROM WORKS_ON WHERE Project_ID = ?;", (project_id,))
        cursor.execute("DELETE FROM GRANT_INFO WHERE Project_ID = ?;", (project_id,))

        # Delete the project.
        cursor.execute("DELETE FROM PROJECT WHERE Project_ID = ?;", (project_id,))

        conn.commit()
        print("Project removed successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error removing project:", e)

    conn.close()


# displays project member menu
def project_member_menu():
    while True:
        print("\n--- Project and Member Management ---")
        print("1. Query all lab members")
        print("2. Add member")
        print("3. Update member")
        print("4. Remove member")
        print("5. Query all projects")
        print("6. Add project")
        print("7. Update project")
        print("8. Remove project")
        print("9. Display project status")
        print("10. Show members who worked on projects funded by a given grant")
        print("11. Show mentorship relations among members on the same project")
        print("12. Back to main menu")

        choice = input("Choose an Option: ")

        if choice == "1":
            query_all_members()
        elif choice == "2":
            add_member()
        elif choice == "3":
            update_member()
        elif choice == "4":
            remove_member()
        elif choice == "5":
            query_all_projects()
        elif choice == "6":
            add_project()
        elif choice == "7":
            update_project_status()
        elif choice == "8":
            remove_project()
        elif choice == "9":
            display_project_status()
        elif choice == "10":
            show_members_by_grant()
        elif choice == "11":
            show_mentorships_same_project()
        elif choice == "12":
            break
        else:
            print("Enter a valid choice.")





def main_menu():
    while True:
        print("\n===== Research Lab Manager =====")
        print("1. Project and Member Management")
        print("2. Equipment Usage Tracking")
        print("3. Grant and Publication Reporting")
        print("4. Exit")
        choice = input("Choose an Option: ")
        if choice == '1':
            project_member_menu()
        elif choice == '2':
            equipment_menu()
        elif choice == '3':
            grantpublication_reporting_menu()
        elif choice == '4':
            print("bye")
            break
        else:
            print("enter a valid choice")




main_menu()