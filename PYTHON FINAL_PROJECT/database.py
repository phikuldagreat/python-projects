#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#ANYTHING DATABASE RELATED
#ESTABLISH CONNECTION, CREATE TABLE, ADD, UPDATE, DELETE CONTENT, ETC.

import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime


class Database:    
    def __init__(self, host="localhost", user="root", password="", database="speak_db"):

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self): #ESTABLISHES CONNECTION TO THE DATABASE
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print(f"Connected to MySQL database: {self.database}")
                return True
                
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def close(self): #CLOSES THE DATABASE CONNECTION
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("MySQL connection closed")
    
    def create_database(self): #CREATE DATABASE IF IT DOESN'T EXIST
        try:
            self._ensure_connection()
            #CONNECT TO MYSQL SERVER W/O DATABASE
            temp_connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            temp_cursor = temp_connection.cursor()
            
            #CREATE DATABASE
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"Database '{self.database}' created/verified")
            
            temp_cursor.close()
            temp_connection.close()
            return True
            
        except Error as e:
            print(f"Error creating database: {e}")
            return False
    
    def create_tables(self): #CREATES NECESSARY TABLES IF THEY DON'T EXIST
        try:
            self._ensure_connection()
            
            self._create_students_table()
            self._create_login_history_table()
            self._create_complaints_table()
            
            self.connection.commit()
            print("✓ Database tables created successfully")
            return True
            
        except Error as e:
            print(f"Error creating tables: {e}")
            return False

    def _create_students_table(self): #CREATES STUDENTS TABLE
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                school_id VARCHAR(6) UNIQUE NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                middle_initial VARCHAR(50),
                last_name VARCHAR(50) NOT NULL,
                contact_number VARCHAR(15) NOT NULL,
                program VARCHAR(100) NOT NULL,
                year_level VARCHAR(10) NOT NULL,
                password_hash VARCHAR(64) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                INDEX idx_school_id (school_id),
                INDEX idx_email (email)
            )
        ''')

    def _create_login_history_table(self): #LOGIN HISTORY TABLE
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        ''')

    def _create_complaints_table(self): #CREATES COMPLAINTS TABLE - NORMALIZED VERSION
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                category VARCHAR(100) NOT NULL,
                complaint VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                status ENUM('Pending', 'In Progress', 'Resolved') DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                INDEX idx_student_id (student_id),
                INDEX idx_status (status),
                INDEX idx_created_at (created_at)
            )
        ''')
    
    @staticmethod
    def hash_password(password): #PASSWORD HASHING FOR PRIVACY AND SECURITY
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_student(self, student_data):
        """
        REGISTERS NEW STUDENT IN THE DATABASE
        
        ARGS:
            student_data (dict): DICTIONARY CONTAINING STUDENT INFO
            
        RETURNS:
            tuple: (success: bool, message: str, student_id: int or None)
        """
        try:
            self._ensure_connection()
            
            # Check for duplicates
            duplicate_check = self._check_duplicate_student(student_data)
            if duplicate_check:
                return duplicate_check
            
            # Insert new student
            student_id = self._insert_student_record(student_data)
            
            return True, "Registration successful!", student_id
            
        except Error as e:
            print(f"Database error: {e}")
            self.connection.rollback()
            return False, "Database error occurred. Please try again.", None

    def _check_duplicate_student(self, student_data):
        """
        CHECKS IF SCHOOL ID OR EMAIL ALREADY EXISTS IN THE DATABASE
        
        RETURNS:
            tuple OR None: (success: bool, message: str) IF DUPLICATE FOUND, ELSE NONE
        """
        #CHECK FOR DUPLICATE SCHOOL ID
        self.cursor.execute(
            "SELECT id FROM students WHERE school_id = %s",
            (student_data['school_id'],)
        )
        if self.cursor.fetchone():
            return False, "School ID already registered.", None
        
        #CHECK FOR DUPLICATE EMAIL
        self.cursor.execute(
            "SELECT id FROM students WHERE email = %s",
            (student_data['email'],)
        )
        if self.cursor.fetchone():
            return False, "Email already registered.", None
        
        return None

    def _insert_student_record(self, student_data):
        """
        #INSERTS NEW STUDENT RECORD INTO THE DATABASE
        
        ARGS:
            student_data (dict): DICTIONARY CONTAINING STUDENT INFO
            
        RETURNS:
            int: NEWLY CREATED STUDENT ID
        """
        password_hash = self.hash_password(student_data['password'])
        
        query = '''
            INSERT INTO students (
                school_id, email, first_name, middle_initial, last_name,
                contact_number, program, year_level, password_hash
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            student_data['school_id'],
            student_data['email'],
            student_data['first_name'],
            student_data['middle_initial'],
            student_data['last_name'],
            student_data['contact_number'],
            student_data['program'],
            student_data['year_level'],
            password_hash
        )
        
        self.cursor.execute(query, values)
        self.connection.commit()
        
        return self.cursor.lastrowid
    
    def authenticate_student(self, school_id, password): #CHECKS IF STUDENT ACC. DETAILS EXIST
        try:
            self._ensure_connection()
            password_hash = self.hash_password(password)
            
            #QUERY DATABASE TO FIND STUDENT
            query = '''
                SELECT id, school_id, email, first_name, middle_initial, 
                       last_name, contact_number, program, year_level
                FROM students 
                WHERE school_id = %s AND password_hash = %s
            '''
            self.cursor.execute(query, (school_id, password_hash))
            user = self.cursor.fetchone()
            
            if user:
                #UPDATE LAST LOGIN TIME
                self.cursor.execute(
                    "UPDATE students SET last_login = NOW() WHERE id = %s",
                    (user['id'],)
                )
                self.connection.commit()
                
                #LOG LOGIN HISTORY
                self.log_login(user['id'])
                
                return True, "Login successful!", dict(user)
            else:
                return False, "Invalid School ID or password.", None
                
        except Error as e:
            print(f"Authentication error: {e}")
            return False, "Authentication error occurred.", None
    
    def log_login(self, student_id, ip_address=None): #LOG STUDENT LOGIN HISTORY
        try:
            self._ensure_connection()
            self.cursor.execute(
                "INSERT INTO login_history (student_id, ip_address) VALUES (%s, %s)",
                (student_id, ip_address)
            )
            self.connection.commit()
        except Error as e:
            print(f"Error logging login: {e}")
    
    def get_student_by_id(self, student_id): #GET STUDENT INFO BY ID
        try:
            self._ensure_connection()
            query = '''
                SELECT id, school_id, email, first_name, middle_initial,
                       last_name, contact_number, program, year_level, created_at
                FROM students WHERE id = %s
            '''
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching student: {e}")
            return None
    
    def update_student_info(self, student_id, update_data): #UPDATE STUDENT PROFILE INFO
        try:
            self._ensure_connection()
            #DYNAMIC UPDATE QUERY
            fields = []
            values = []
            
            for key, value in update_data.items():
                if key != 'password':
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return False, "No fields to update"
            
            values.append(student_id)
            query = f"UPDATE students SET {', '.join(fields)} WHERE id = %s"
            
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            
            return True, "Profile updated successfully!"
            
        except Error as e:
            print(f"Update error: {e}")
            self.connection.rollback()
            return False, "Error updating profile."
    
    def change_password(self, student_id, old_password, new_password): #CHANGE CURRENT PASSWORD TO NEW PASSWORD
        try:
            self._ensure_connection()
            #VERIFY OLD PASSWORD
            old_hash = self.hash_password(old_password)
            self.cursor.execute(
                "SELECT id FROM students WHERE id = %s AND password_hash = %s",
                (student_id, old_hash)
            )
            
            if not self.cursor.fetchone():
                return False, "Current password is incorrect."
            
            #UPDATE TO NEW PASS
            new_hash = self.hash_password(new_password)
            self.cursor.execute(
                "UPDATE students SET password_hash = %s WHERE id = %s",
                (new_hash, student_id)
            )
            self.connection.commit()
            
            return True, "Password changed successfully!"
            
        except Error as e:
            print(f"Password change error: {e}")
            self.connection.rollback()
            return False, "Error changing password."

    def submit_complaint(self, complaint_data):
        """
        SUBMIT NEW COMPLAINT - NORMALIZED VERSION WITHOUT REDUNDANT DATA
        """
        try:
            self._ensure_connection()
            #GET STUDENT_ID FROM SCHOOL_ID
            self.cursor.execute(
                "SELECT id FROM students WHERE school_id = %s",
                (complaint_data['school_id'],)
            )
            student = self.cursor.fetchone()
            
            if not student:
                return False, "Student not found.", None
            
            query = '''
                INSERT INTO complaints (
                    student_id, category, complaint, location, description, status
                ) VALUES (%s, %s, %s, %s, %s, 'Pending')
            '''
            values = (
                student['id'],
                complaint_data['category'],
                complaint_data['complaint'],
                complaint_data['location'],
                complaint_data['description']
            )
            
            self.cursor.execute(query, values)
            self.connection.commit()
            complaint_id = self.cursor.lastrowid
            
            return True, "Complaint submitted successfully!", complaint_id
            
        except Error as e:
            print(f"Error submitting complaint: {e}")
            self.connection.rollback()
            return False, "Error submitting complaint.", None

    def get_student_complaints(self, school_id):
        """
        GET ALL COMPLAINTS FOR A STUDENT - JOINS WITH STUDENTS TABLE
        """
        try:
            self._ensure_connection()
            query = '''
                SELECT c.id, c.category, c.complaint, c.location, c.status, 
                    DATE_FORMAT(c.created_at, '%Y-%m-%d') as date,
                    c.description
                FROM complaints c
                INNER JOIN students s ON c.student_id = s.id
                WHERE s.school_id = %s
                ORDER BY c.created_at DESC
            '''
            self.cursor.execute(query, (school_id,))
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"Error fetching complaints: {e}")
            return []

    def get_all_complaints(self):
        """
        GET ALL COMPLAINTS WITH STUDENT INFO - JOINS WITH STUDENTS TABLE
        """
        try:
            self._ensure_connection()
            query = '''
                SELECT c.id, s.school_id, s.program, c.complaint, 
                    c.status, DATE_FORMAT(c.created_at, '%Y-%m-%d') as date,
                    c.category, c.location, c.description
                FROM complaints c
                INNER JOIN students s ON c.student_id = s.id
                ORDER BY c.created_at DESC
            '''
            self.cursor.execute(query)
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"Error fetching all complaints: {e}")
            return []

    def update_complaint(self, complaint_id, complaint_data):
        try:
            self._ensure_connection()
            query = '''
                UPDATE complaints 
                SET category = %s, complaint = %s, location = %s, description = %s
                WHERE id = %s AND status = 'Pending'
            '''
            values = (
                complaint_data['category'],
                complaint_data['complaint'],
                complaint_data['location'],
                complaint_data['description'],
                complaint_id
            )
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return True, "Complaint updated successfully!"
            else:
                return False, "Cannot update complaint (may not be pending)."
            
        except Error as e:
            print(f"Error updating complaint: {e}")
            self.connection.rollback()
            return False, "Error updating complaint."

    def delete_complaint(self, complaint_id):
        try:
            self._ensure_connection()
            query = "DELETE FROM complaints WHERE id = %s AND status = 'Pending'"
            self.cursor.execute(query, (complaint_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return True, "Complaint deleted successfully!"
            else:
                return False, "Cannot delete complaint (may not be pending)."
            
        except Error as e:
            print(f"Error deleting complaint: {e}")
            self.connection.rollback()
            return False, "Error deleting complaint."

    def update_complaint_status(self, complaint_id, new_status):
        try:
            self._ensure_connection()
            query = "UPDATE complaints SET status = %s WHERE id = %s"
            self.cursor.execute(query, (new_status, complaint_id))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return True, f"Complaint marked as {new_status}!"
            else:
                return False, "Complaint not found."
            
        except Error as e:
            print(f"Error updating status: {e}")
            self.connection.rollback()
            return False, "Error updating status."

    def reset_student_password(self, school_id, email, new_password): #RESET PASSWORD FOR STUDENT ACCOUNT
        try:
            self._ensure_connection()
            
            #VERIFY SCHOOL ID AND EMAIL MATCH
            query = '''
                SELECT id FROM students 
                WHERE school_id = %s AND email = %s
            '''
            self.cursor.execute(query, (school_id, email))
            result = self.cursor.fetchone()
            
            if not result:
                return False, "School ID and email do not match our records."
            
            student_id = result['id']
            
            #HASH THE NEW PASSWORD
            new_password_hash = self.hash_password(new_password)
            
            #UPDATE PASSWORD
            update_query = '''
                UPDATE students 
                SET password_hash = %s 
                WHERE id = %s
            '''
            self.cursor.execute(update_query, (new_password_hash, student_id))
            self.connection.commit()
            
            return True, "Password reset successful! You can now login with your new password."
            
        except Error as e:
            print(f"Error resetting password: {e}")
            self.connection.rollback()
            return False, f"Error resetting password: {str(e)}"

    def _ensure_connection(self): #CHECK DATABASE CONNECTION
        try:
            if self.connection is None or not self.connection.is_connected():
                print("⚠ Connection lost, reconnecting...")
                self.connect()
                return True
            #PING TO KEEP CONNECTION ALIVE
            self.connection.ping(reconnect=True, attempts=3, delay=1)
            return True
        except Error as e:
            print(f"Connection check failed: {e}")
            return self.connect()
        
    def get_login_history(self, student_id, limit=50): #GET LOGIN HISTORY FOR A STUDENT
        try:
            self._ensure_connection()
            
            query = '''
                SELECT login_time, ip_address
                FROM login_history
                WHERE student_id = %s
                ORDER BY login_time DESC
                LIMIT %s
            '''
            self.cursor.execute(query, (student_id, limit))
            results = self.cursor.fetchall()
            
            formatted_results = []
            for row in results:
                formatted_results.append({
                    'login_time': row['login_time'].strftime('%Y-%m-%d %H:%M:%S') if row['login_time'] else 'N/A',
                    'ip_address': row['ip_address']
                })
            
            return formatted_results
        except Error as e:
            print(f"Error fetching login history: {e}")
            import traceback
            traceback.print_exc()
            return []