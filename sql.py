import sqlite3
from constants import DATABASE, PROFILE_TABLE

# SQL statement to create the "profile" table if it does not exist
CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    name TEXT,
    specialization TEXT,
    tsc_attended TEXT,
    completion_year INTEGER,
    digital_address TEXT,
    email TEXT,
    telephone TEXT,
    city TEXT,
    region TEXT,
    country TEXT,
    current_job_title TEXT,
    current_employer TEXT,
    industry_or_sector TEXT
);
'''

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    """
    Connect to the SQLite database and create the table if it does not exist.
    """
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the SQL statement to create the table
        cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        print("Database and table checked/created successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred while working with the database: {e}")

def save_profiles(profiles_to_insert):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use placeholders (?) for each column
    query = '''
        INSERT INTO profile (student_id, name, specialization, tsc_attended, completion_year, digital_address, email, telephone, city, region, country, current_job_title, current_employer, industry_or_sector)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    try:
        # Insert the profiles
        cursor.executemany(query, profiles_to_insert)
        conn.commit()
        print("Profiles inserted successfully.")
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()


def save_profile(student_id, name, specialization, tsc_attended, completion_year, digital_address, email, telephone, city, region, country,
         job_title, employer, industry):
    conn = get_db_connection()
    conn.execute(
        '''INSERT INTO profile 
        (student_id, name, specialization, tsc_attended, completion_year, digital_address, email, telephone, city, region, country, current_job_title, current_employer, industry_or_sector)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (student_id, name, specialization, tsc_attended, completion_year, digital_address, email, telephone, city, region, country,
         job_title, employer, industry)
    )
    conn.commit()
    conn.close()

def get_all_profiles():
    conn = get_db_connection()
    profiles = conn.execute('SELECT * FROM profile').fetchall()
    conn.close()
    return profiles
