import sqlite3

DB_NAME = "lab.db"

def connect():
    """ Connects python to the SQLite database"""
    return sqlite3.connect(DB_NAME)

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

def top5projectsbygrant():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            P.Project_ID,
            P.Title,
            G.Budget
        FROM PROJECT AS P
        JOIN GRANT_INFO AS G
            ON P.Project_ID = G.Project_ID
        ORDER BY G.BUDGET DESC
        LIMIT 5;
    """)
    results = cursor.fetchall()

    if results:
        print("\n--- Top 5 projects by grant ---")
        for row in results:
            print(
                f"Project ID: {row[0]} | "
                f"Project: {row[1]} | "
                f"Budget: {row[2]}"
            )
    else:
        print("No mentorship relations found among members on the same project.")

    conn.close()


# displays project member menu
def project_member_menu():
    while True:
        print("\n--- Project and Member Management ---")
        print("1. Query all lab members")
        print("2. Display project status")
        print("3. Query all projects")
        print("4. Show members who worked on projects funded by a given grant")
        print("5. Show mentorship relations among members on the same project")
        print("6. Back to main menu")

        choice = input("Choose an Option: ")

        if choice == "1":
            query_all_members()
        elif choice == "2":
            display_project_status()
        elif choice == '3':
            query_all_projects()
        elif choice == '4':
            show_members_by_grant()
        elif choice == '5':
            show_mentorships_same_project()
        elif choice == "6":
            break
        else:
            print("Enter a valid choice.")
def grantpublication_reporting_menu():
    while True:
        print("\n--- Grant and Publication Reporting ---")
        print("1. List top 5 projects")
        '''
        List the top 5 projects ranked by their total grant funding, and show the total
        amount each project received, in decreasing order of total funding (assume
        Budget is the dollar amount of each grant).
        '''
        print("2. Find the Mentor whos mentees produced the most publications")
        #self explanitory
        print("3. Calculate total number of student publications per major and per publications")
        #self explanitory
        print("4. Find projects that ended before date X and the number of grants that funded each project")

        print("5. Find the three most productive years in terms of publications produced by students")
        print("6. Back to main menu")
        choice = input("Choose an Option: ")
        if choice == "1":
            top5projectsbygrant()
        elif choice == "2":
            break
        elif choice == '3':
            break
        elif choice == '4':
            break
        elif choice == '5':
            break
        elif choice == "6":
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
        choice = int(input("Choose an Option: "))
        if choice == 1:
            project_member_menu()
        elif choice == 2:
            display_project_status()
        elif choice == 3:
            grantpublication_reporting_menu()
        elif choice == 4:
            print("bye")
            break
        else:
            print("enter a valid choice")

main_menu()