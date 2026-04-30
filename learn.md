# Delieverable 3

- The goal of the project is build a **database system application** for the university lab reserach. 
    - so we are deisgning a system that can store and manage infromation about all the relations. 

- A DBMS is software that helps you create, store, update, delete, and query data.
    - database is your stored data
    - and the DBMS is what allows us to manage that stored data 

- FOr the DMBS we will be using SQLite because:
    - it works well with python
    - doesnt need serves
    
- SQL will be the way we will be able to talk to the DMBS to modify the databases. 

- And we will use python as the lanaguge to send these SQL commands to the DBMS. 

- User chooses something in the Python menu
-        ↓
- Python runs a SQL command
-        ↓
- SQLite receives that SQL command
-        ↓
- SQLite reads or modifies lab.db
-        ↓
- Python shows the result back to the user

## commands
- ` sqlite3 lab.db < schema.sql`
    - creates a lab.db database file and runs all the sql commands which allows the DMBSt to create the tables 
-`sqlite3 lab.db`
    - Opens the database using sqlite 
    - it allows us to type commands inside sqlite directly