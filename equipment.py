import sqlite3

DB_NAME = "lab.db"


def connect():
    """Connects Python to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def blank_to_none(value):
    value = value.strip()
    if value == "":
        return None
    return value


def query_all_equipment():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            E.EID,
            E.Name,
            E.Type,
            E.Manual,
            D.Device_ID,
            D.Status,
            D.Purchase_Date
        FROM EQUIPMENT AS E
        LEFT JOIN DEVICE AS D
            ON E.EID = D.EID
        ORDER BY E.EID, D.Device_ID;
    """)

    results = cursor.fetchall()

    if results:
        print("\n--- All Equipment and Devices ---")
        for row in results:
            print(
                f"EID: {row[0]} | "
                f"Equipment: {row[1]} | "
                f"Type: {row[2]} | "
                f"Device ID: {row[4]} | "
                f"Status: {row[5]} | "
                f"Purchase Date: {row[6]}"
            )
    else:
        print("No equipment found.")

    conn.close()


def add_equipment():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Add Equipment ---")

    eid = input("Enter Equipment ID: ")
    equipment_type = input("Enter Equipment Type: ")
    name = input("Enter Equipment Name: ")
    manual = input("Enter Manual Description: ")

    try:
        cursor.execute("""
            INSERT INTO EQUIPMENT
            (EID, Type, Name, Manual)
            VALUES (?, ?, ?, ?);
        """, (eid, equipment_type, name, manual))

        conn.commit()
        print("Equipment added successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error adding equipment:", e)

    conn.close()


def add_device():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Add Device for Equipment ---")

    eid = input("Enter Equipment ID: ")
    device_id = input("Enter Device ID: ")
    status = input("Enter Status (available, in use, retired): ")
    purchase_date = blank_to_none(input("Enter Purchase Date (YYYY-MM-DD): "))

    try:
        cursor.execute("""
            INSERT INTO DEVICE
            (EID, Device_ID, Status, Purchase_Date)
            VALUES (?, ?, ?, ?);
        """, (eid, device_id, status, purchase_date))

        conn.commit()
        print("Device added successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error adding device:", e)

    conn.close()


def update_equipment():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Update Equipment ---")
    eid = input("Enter Equipment ID to update: ")

    cursor.execute("""
        SELECT EID, Type, Name, Manual
        FROM EQUIPMENT
        WHERE EID = ?;
    """, (eid,))

    equipment = cursor.fetchone()

    if not equipment:
        print("No equipment found with that ID.")
        conn.close()
        return

    print("Press Enter to keep the current value.")

    new_type = input(f"Enter new type [{equipment[1]}]: ")
    new_name = input(f"Enter new name [{equipment[2]}]: ")
    new_manual = input(f"Enter new manual [{equipment[3]}]: ")

    new_type = equipment[1] if new_type.strip() == "" else new_type
    new_name = equipment[2] if new_name.strip() == "" else new_name
    new_manual = equipment[3] if new_manual.strip() == "" else new_manual

    cursor.execute("""
        UPDATE EQUIPMENT
        SET Type = ?,
            Name = ?,
            Manual = ?
        WHERE EID = ?;
    """, (new_type, new_name, new_manual, eid))

    conn.commit()
    print("Equipment updated successfully.")
    conn.close()


def update_device_status():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Update Device Status ---")
    eid = input("Enter Equipment ID: ")
    device_id = input("Enter Device ID: ")
    new_status = input("Enter new status (available, in use, retired): ")

    try:
        cursor.execute("""
            UPDATE DEVICE
            SET Status = ?
            WHERE EID = ? AND Device_ID = ?;
        """, (new_status, eid, device_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Device status updated successfully.")
        else:
            print("No device found with that Equipment ID and Device ID.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error updating device status:", e)

    conn.close()


def remove_equipment():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Remove Equipment ---")
    eid = input("Enter Equipment ID to remove: ")

    cursor.execute("""
        SELECT Name
        FROM EQUIPMENT
        WHERE EID = ?;
    """, (eid,))

    equipment = cursor.fetchone()

    if not equipment:
        print("No equipment found with that ID.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to remove equipment '{equipment[0]}' and all its devices/usages? (y/n): ")

    if confirm.lower() != "y":
        print("Remove canceled.")
        conn.close()
        return

    try:
        cursor.execute("DELETE FROM IS_USED WHERE EID = ?;", (eid,))
        cursor.execute("DELETE FROM DEVICE WHERE EID = ?;", (eid,))
        cursor.execute("DELETE FROM EQUIPMENT WHERE EID = ?;", (eid,))

        conn.commit()
        print("Equipment removed successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error removing equipment:", e)

    conn.close()


def query_all_usage():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            IU.EID,
            E.Name,
            IU.Device_ID,
            IU.Member_ID,
            L.Member_Name,
            IU.Start_Date,
            IU.End_Date,
            IU.Purpose
        FROM IS_USED AS IU
        JOIN EQUIPMENT AS E
            ON IU.EID = E.EID
        JOIN LAB_MEMBER AS L
            ON IU.Member_ID = L.Member_ID
        ORDER BY IU.EID, IU.Device_ID, IU.Start_Date;
    """)

    results = cursor.fetchall()

    if results:
        print("\n--- Equipment Usage Records ---")
        for row in results:
            end_date = row[6] if row[6] is not None else "Currently in use"
            print(
                f"EID: {row[0]} | "
                f"Equipment: {row[1]} | "
                f"Device ID: {row[2]} | "
                f"Member ID: {row[3]} | "
                f"Member: {row[4]} | "
                f"Start: {row[5]} | "
                f"End: {end_date} | "
                f"Purpose: {row[7]}"
            )
    else:
        print("No usage records found.")

    conn.close()


def add_usage():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Add Equipment Usage ---")

    eid = input("Enter Equipment ID: ")
    device_id = input("Enter Device ID: ")
    member_id = input("Enter Member ID: ")
    start_date = input("Enter Usage Start Date (YYYY-MM-DD): ")
    end_date = blank_to_none(input("Enter Usage End Date or press Enter if currently in use: "))
    purpose = input("Enter Purpose of Use: ")

    try:
        if end_date is None:
            cursor.execute("""
                SELECT COUNT(*)
                FROM IS_USED
                WHERE EID = ?
                  AND Device_ID = ?
                  AND End_Date IS NULL;
            """, (eid, device_id))

            active_count = cursor.fetchone()[0]

            if active_count >= 3:
                print("Cannot add usage. This device already has 3 active users.")
                conn.close()
                return

        cursor.execute("""
            INSERT INTO IS_USED
            (EID, Device_ID, Member_ID, Start_Date, End_Date, Purpose)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (eid, device_id, member_id, start_date, end_date, purpose))

        if end_date is None:
            cursor.execute("""
                UPDATE DEVICE
                SET Status = 'in use'
                WHERE EID = ? AND Device_ID = ?;
            """, (eid, device_id))

        conn.commit()
        print("Equipment usage added successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error adding usage:", e)

    conn.close()


def update_usage():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Update Equipment Usage ---")
    print("To identify the usage record, enter EID, Device ID, Member ID, and Start Date.")

    eid = input("Enter Equipment ID: ")
    device_id = input("Enter Device ID: ")
    member_id = input("Enter Member ID: ")
    start_date = input("Enter original Start Date (YYYY-MM-DD): ")

    cursor.execute("""
        SELECT End_Date, Purpose
        FROM IS_USED
        WHERE EID = ?
          AND Device_ID = ?
          AND Member_ID = ?
          AND Start_Date = ?;
    """, (eid, device_id, member_id, start_date))

    usage = cursor.fetchone()

    if not usage:
        print("No usage record found.")
        conn.close()
        return

    print("Press Enter to keep the current value.")

    new_end_date = input(f"Enter new End Date [{usage[0]}]: ")
    new_purpose = input(f"Enter new Purpose [{usage[1]}]: ")

    new_end_date = usage[0] if new_end_date.strip() == "" else blank_to_none(new_end_date)
    new_purpose = usage[1] if new_purpose.strip() == "" else new_purpose

    try:
        cursor.execute("""
            UPDATE IS_USED
            SET End_Date = ?,
                Purpose = ?
            WHERE EID = ?
              AND Device_ID = ?
              AND Member_ID = ?
              AND Start_Date = ?;
        """, (new_end_date, new_purpose, eid, device_id, member_id, start_date))

        if new_end_date is not None:
            cursor.execute("""
                SELECT COUNT(*)
                FROM IS_USED
                WHERE EID = ?
                  AND Device_ID = ?
                  AND End_Date IS NULL;
            """, (eid, device_id))

            active_count = cursor.fetchone()[0]

            if active_count == 0:
                cursor.execute("""
                    UPDATE DEVICE
                    SET Status = 'available'
                    WHERE EID = ? AND Device_ID = ?;
                """, (eid, device_id))

        conn.commit()
        print("Usage record updated successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error updating usage:", e)

    conn.close()


def remove_usage():
    conn = connect()
    cursor = conn.cursor()

    print("\n--- Remove Equipment Usage ---")
    print("To identify the usage record, enter EID, Device ID, Member ID, and Start Date.")

    eid = input("Enter Equipment ID: ")
    device_id = input("Enter Device ID: ")
    member_id = input("Enter Member ID: ")
    start_date = input("Enter Start Date (YYYY-MM-DD): ")

    try:
        cursor.execute("""
            DELETE FROM IS_USED
            WHERE EID = ?
              AND Device_ID = ?
              AND Member_ID = ?
              AND Start_Date = ?;
        """, (eid, device_id, member_id, start_date))

        if cursor.rowcount == 0:
            print("No usage record found.")
            conn.close()
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM IS_USED
            WHERE EID = ?
              AND Device_ID = ?
              AND End_Date IS NULL;
        """, (eid, device_id))

        active_count = cursor.fetchone()[0]

        if active_count == 0:
            cursor.execute("""
                UPDATE DEVICE
                SET Status = 'available'
                WHERE EID = ? AND Device_ID = ?;
            """, (eid, device_id))

        conn.commit()
        print("Usage record removed successfully.")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Error removing usage:", e)

    conn.close()


def show_equipment_status():
    conn = connect()
    cursor = conn.cursor()

    eid = input("Enter Equipment ID: ")

    cursor.execute("""
        SELECT
            E.EID,
            E.Name,
            E.Type,
            D.Device_ID,
            D.Status,
            D.Purchase_Date
        FROM EQUIPMENT AS E
        JOIN DEVICE AS D
            ON E.EID = D.EID
        WHERE E.EID = ?
        ORDER BY D.Device_ID;
    """, (eid,))

    results = cursor.fetchall()

    if results:
        print("\n--- Equipment Status ---")
        for row in results:
            print(
                f"EID: {row[0]} | "
                f"Equipment: {row[1]} | "
                f"Type: {row[2]} | "
                f"Device ID: {row[3]} | "
                f"Status: {row[4]} | "
                f"Purchase Date: {row[5]}"
            )
    else:
        print("No equipment found with that ID.")

    conn.close()


def show_current_users_for_equipment():
    conn = connect()
    cursor = conn.cursor()

    eid = input("Enter Equipment ID: ")

    cursor.execute("""
        SELECT DISTINCT
            E.EID,
            E.Name,
            D.Device_ID,
            L.Member_ID,
            L.Member_Name,
            P.Project_ID,
            P.Title,
            W.Role,
            IU.Start_Date,
            IU.Purpose
        FROM EQUIPMENT AS E
        JOIN DEVICE AS D
            ON E.EID = D.EID
        JOIN IS_USED AS IU
            ON D.EID = IU.EID
            AND D.Device_ID = IU.Device_ID
        JOIN LAB_MEMBER AS L
            ON IU.Member_ID = L.Member_ID
        JOIN WORKS_ON AS W
            ON L.Member_ID = W.Member_ID
        JOIN PROJECT AS P
            ON W.Project_ID = P.Project_ID
        WHERE E.EID = ?
          AND IU.End_Date IS NULL
        ORDER BY D.Device_ID, L.Member_ID, P.Project_ID;
    """, (eid,))

    results = cursor.fetchall()

    if results:
        print("\n--- Current Users and Their Projects ---")
        for row in results:
            print(
                f"EID: {row[0]} | "
                f"Equipment: {row[1]} | "
                f"Device ID: {row[2]} | "
                f"Member ID: {row[3]} | "
                f"Member: {row[4]} | "
                f"Project ID: {row[5]} | "
                f"Project: {row[6]} | "
                f"Role: {row[7]} | "
                f"Usage Start: {row[8]} | "
                f"Purpose: {row[9]}"
            )
    else:
        print("No current users found for that equipment.")

    conn.close()


def equipment_menu():
    while True:
        print("\n--- Equipment Usage Tracking ---")
        print("1. Query all equipment and devices")
        print("2. Add equipment")
        print("3. Add device for equipment")
        print("4. Update equipment")
        print("5. Update device status")
        print("6. Remove equipment")
        print("7. Query all equipment usage")
        print("8. Add equipment usage")
        print("9. Update equipment usage")
        print("10. Remove equipment usage")
        print("11. Show status of a piece of equipment")
        print("12. Show current users of equipment and their projects")
        print("13. Back to main menu")

        choice = input("Choose an Option: ")

        if choice == "1":
            query_all_equipment()
        elif choice == "2":
            add_equipment()
        elif choice == "3":
            add_device()
        elif choice == "4":
            update_equipment()
        elif choice == "5":
            update_device_status()
        elif choice == "6":
            remove_equipment()
        elif choice == "7":
            query_all_usage()
        elif choice == "8":
            add_usage()
        elif choice == "9":
            update_usage()
        elif choice == "10":
            remove_usage()
        elif choice == "11":
            show_equipment_status()
        elif choice == "12":
            show_current_users_for_equipment()
        elif choice == "13":
            break
        else:
            print("Enter a valid choice.")