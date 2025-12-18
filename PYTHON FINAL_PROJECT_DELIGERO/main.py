#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#MAIN APPLICATION FILE

from PyQt6.QtWidgets import QApplication
from auth_gui import LoginWindow, RegisterWindow, ForgotPasswordDialog
from admin_gui import AdminDashboard
from student_gui import StudentDashboard
from auth_logic import AuthService


class AuthController:
    
    def __init__(self):
        self.auth_service = AuthService()
        self.login_window = LoginWindow()
        self.register_window = RegisterWindow()
        self.admin_dashboard = AdminDashboard()
        
        self.student_dashboard = None  #STUDENT DASHBOARD IS INITIALIZED AS NONE
        
        self._connect_signals()
        
    def _connect_signals(self): #SIGNALS TO CALL GUI METHODS
        #LOGIN WINDOW SIGNALS
        self.login_window.login_clicked.connect(self.handle_login)
        self.login_window.register_requested.connect(self.show_register_window)
        self.login_window.admin_login_requested.connect(self.handle_admin_login)
        self.login_window.forgot_password_requested.connect(self.handle_forgot_password)
        
        #REGISTER WINDOW SIGNALS
        self.register_window.registration_complete.connect(self.handle_registration)
        self.register_window.back_to_login.connect(self.show_login_window)
        
        #ADMIN DASHBOARD SIGNALS
        self.admin_dashboard.logout_requested.connect(self.show_login_window)
    
    def handle_login(self, username, password): #HANDLES LOGIN FOR STUDENT
        if username.lower() == "admin":
            self.handle_admin_login(password) #IF USERNAME IS ADMIN, CALL ADMIN LOGIN METHOD
            return
            
        success, message, user_data = self.auth_service.login(username, password)
        
        if success:
            #HIDE LOGIN WINDOW AND CLEAR FIELDS
            self.login_window.hide()
            self.login_window.clear_fields()
            
            #CREATE NEW STUDENT DASHBOARD INSTANCE
            self.student_dashboard = StudentDashboard(user_data, self.auth_service.db)
            
            #CONNECT LOGOUT SIGNAL
            self.student_dashboard.logout_requested.connect(self.show_login_window)
            
            #SHOW STUDENT DASHBOARD
            self.student_dashboard.showFullScreen()
        else:
            self.login_window.show_error("Login Failed", message)
    
    def handle_admin_login(self, password): #HANDLES ADMIN LOGIN
        if password == "admin123":
            print("Admin password correct")
            self.login_window.hide()
            self.login_window.clear_fields()
            self.admin_dashboard.set_admin("Administrator")
            print("Loading complaints...")
            self.admin_dashboard.load_complaints()
            print("Complaints loaded successfully")
            self.admin_dashboard.showFullScreen()
        else:
            self.login_window.show_error("Access Denied", "Invalid admin credentials")
    
    def handle_registration(self, student_data): #PROCESS REGISTRATION DATA
        try:
            success, message = self.auth_service.register(student_data)
            
            if success:
                self.register_window.show_success("Registration Successful", message)
                self.show_login_window()
            else:
                self.register_window.show_error("Registration Failed", message)
        except Exception as e:
            print(f"Registration error: {e}")
            import traceback
            traceback.print_exc()
            self.register_window.show_error("Error", f"An error occurred: {str(e)}")
    
    def handle_forgot_password(self): #HANDLE PASSWORD RESET
        dialog = ForgotPasswordDialog(self.login_window)
        
        if dialog.exec():
            reset_data = dialog.get_reset_data()
            success, message = self.auth_service.reset_password(reset_data)
            
            if success:
                self.login_window.show_success("Password Reset", message)
            else:
                self.login_window.show_error("Reset Failed", message)
    
    def show_register_window(self): #SHOWS REGISTRATION WINDOW
        self.login_window.hide()
        self.register_window.show()
    
    def show_login_window(self): #SHOWS LOGIN WINDOW
        self.register_window.hide()
        self.admin_dashboard.hide()
        
        #HIDE STUDENT DASHBOARD IF IT EXISTS
        if self.student_dashboard:
            self.student_dashboard.hide()
        
        self.register_window.clear_fields()
        self.login_window.show()
    
    def start(self):
        self.login_window.show()


def main():
    app = QApplication([])
    controller = AuthController()
    controller.start()
    app.exec()


if __name__ == "__main__":
    main()