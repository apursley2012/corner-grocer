####################################################################
#  db_handler.py                                                   #
#  Name: Alysha Pursley                                            #
#  Date: August 3, 2025                                            #
#  Description:                                                    #
#    Handles all database operations for grocery frequency         #
####################################################################

import sqlite3
import sys

####################################################################
#  Connect to SQLite Database                                      #
#  Establishes and returns connection object, creating DB if not   #
#  found                                                           #
####################################################################
def connect_to_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to database: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

####################################################################
#  Create Frequency Table                                          #
#  Creates table if it doesn't already exist                       #
####################################################################
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grocery_frequency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL UNIQUE,
                frequency INTEGER NOT NULL
            );
        """)
        conn.commit()
        print("Verified or created grocery_frequency table.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        sys.exit(1)

####################################################################
#  Insert or Update Item Frequency                                 #
#  If item exists, increment frequency; otherwise insert new       #
####################################################################
def insert_or_update_item(conn, item):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT frequency FROM grocery_frequency WHERE item_name = ?;",
            (item,)
        )
        result = cursor.fetchone()
        if result:
            new_count = result[0] + 1
            cursor.execute(
                "UPDATE grocery_frequency SET frequency = ? WHERE item_name = ?;",
                (new_count, item)
            )
        else:
            cursor.execute(
                "INSERT INTO grocery_frequency (item_name, frequency) VALUES (?, 1);",
                (item,)
            )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting/updating item '{item}': {e}")

####################################################################
#  Retrieve All Frequencies                                        #
#  Returns dict of all items & frequencies, sorted alphabetically  #
####################################################################
def get_all_frequencies(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT item_name, frequency FROM grocery_frequency ORDER BY item_name ASC;"
        )
        rows = cursor.fetchall()
        return {item: freq for item, freq in rows}
    except sqlite3.Error as e:
        print(f"Error retrieving all frequencies: {e}")
        return {}

####################################################################
#  Retrieve Frequency for Specific Item                            #
#  Returns frequency if found, else 0                              #
####################################################################
def get_frequency_for_item(conn, item):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT frequency FROM grocery_frequency WHERE item_name = ?;",
            (item,)
        )
        result = cursor.fetchone()
        return result[0] if result else 0
    except sqlite3.Error as e:
        print(f"Error retrieving frequency for '{item}': {e}")
        return 0

####################################################################
#  Retrieve Frequencies Sorted by Count                            #
#  Returns dict sorted by frequency desc, then A–Z for ties        #
####################################################################
def get_frequencies_sorted_by_count(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_name, frequency
            FROM grocery_frequency
            ORDER BY frequency DESC, item_name ASC;
        """)
        rows = cursor.fetchall()
        return {item: freq for item, freq in rows}
    except sqlite3.Error as e:
        print(f"Error retrieving sorted frequencies: {e}")
        return {}

####################################################################
#  Clear all data from the table                                   #
#  Used for resetting the database                                 #
####################################################################
def clear_all_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grocery_frequency;")
        conn.commit()
        print("All data cleared from database.")
    except sqlite3.Error as e:
        print(f"Error clearing data: {e}")