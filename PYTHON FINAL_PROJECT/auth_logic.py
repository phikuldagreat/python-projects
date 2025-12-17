#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#HANDLES ALL LOGIC RELATED TO AUTHENTICATION

from database import Database
from config import DB_CONFIG
import re

class AuthValidator: #VALIDATOR FOR AUTH LOGIC
    
    @staticmethod
    def validate_login(username, password): #VALIDATE LOGIN DATA
        if not username or not password:
            return False, "Please enter both School ID and password."
        
        if len(username) < 6:
            return False, "School ID must be at least 6 characters."
            
        return True, None
    
    @staticmethod
    def validate_registration(student_data): #VALIDATE REGISTRATION DATA
        required_fields = ['school_id', 'email', 'first_name', 'last_name', 
                          'contact_number', 'password']
        
        for field in required_fields:
            if not student_data.get(field):
                return False, "Please fill in all required fields marked with <span style='color: red;'>*</span>"
        
        email = student_data['email']
        if '@' not in email or '.' not in email or '@umindanao.edu.ph' not in email:
            return False, "Please enter a valid email address."
        
        password = student_data['password']
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one number."
        
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter."
        
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter."
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character."
        
        if student_data['password'] != student_data.get('confirm_password'):
            return False, "Passwords do not match. Please try again."
        
        school_id = student_data['school_id']
        if len(school_id) < 6:
            return False, "Please enter a valid School ID."
        
        contact = student_data['contact_number']
        if len(contact) < 10:
            return False, "Please enter a valid contact number."
        
        return True, None
    
    @staticmethod
    def validate_password_reset(reset_data): #VALIDATE PASSWORD RESET DATA
        if not reset_data.get('school_id'):
            return False, "Please enter your School ID."
        
        if not reset_data.get('email'):
            return False, "Please enter your email."
        
        email = reset_data['email']
        if '@umindanao.edu.ph' not in email:
            return False, "Please enter a valid school email."
        
        new_password = reset_data.get('new_password', '')
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long."
        
        if new_password != reset_data.get('confirm_password'):
            return False, "Passwords do not match."
        
        return True, None


class AuthService: #AUTHENTICATION SERVICE
    
    def __init__(self):
        self.validator = AuthValidator()
        self.db = Database(**DB_CONFIG)
        
    def login(self, username, password): #LOGIN ATTEMPT VALIDATOR

        is_valid, error = self.validator.validate_login(username, password)
        if not is_valid:
            return False, error, None
        
        if not self.db.connect():
            return False, "Database connection error.", None
        
        success, message, user_data = self.db.authenticate_student(username, password)
        
        self.db.close()
        return success, message, user_data
    
    def register(self, student_data): #REGISTER NEW STUDENT
        
        is_valid, error = self.validator.validate_registration(student_data)
        if not is_valid:
            return False, error
        
        if not self.db.connect():
            return False, "Database connection error."
        
        success, message, student_id = self.db.register_student(student_data)
        
        self.db.close()
        
        if success:
            return True, f"Registration successful! Welcome, {student_data['first_name']}!"
        else:
            return False, message
    
    def reset_password(self, reset_data): #RESET PASSWORD FOR EXISTING STUDENT
        
        is_valid, error = self.validator.validate_password_reset(reset_data)
        if not is_valid:
            return False, error
        
        if not self.db.connect():
            return False, "Database connection error."
        
        success, message = self.db.reset_student_password(
            reset_data['school_id'],
            reset_data['email'],
            reset_data['new_password']
        )
        
        self.db.close()
        return success, message