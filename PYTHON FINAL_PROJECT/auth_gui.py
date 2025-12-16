#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#LOGIN AND REGISTRATION WINDOW GUI

from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QMessageBox, QComboBox, QScrollArea, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon
from theme import ColorTheme, StyleSheet


#CUSTOM PASSWORD INPUT WITH TOGGLE INSIDE
class PasswordInput(QLineEdit):
    def __init__(self, placeholder_text="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_visible = False
        
        #CREATE TOGGLE BUTTON
        self.toggle_btn = QPushButton("Show", self)
        self.toggle_btn.setFlat(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setFixedSize(30, 30)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 9px;
                color: #666;
                padding: 0px 4px;
            }
            QPushButton:hover {
                color: #000;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)
        
        self._update_button_position()
    
    def toggle_password_visibility(self): #TOGGLE PASSWORD VISIBILITY
        if self.password_visible:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("Show")
            self.password_visible = False
        else:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Hide")
            self.password_visible = True
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_button_position()
    
    def _update_button_position(self):
        button_size = self.toggle_btn.size()
        frame_width = self.style().pixelMetric(self.style().PixelMetric.PM_DefaultFrameWidth)
        self.toggle_btn.move(
            self.rect().right() - button_size.width() - frame_width - 5,
            (self.rect().bottom() - button_size.height()) // 2
        )

        self.setTextMargins(0, 0, button_size.width() + 10, 0)

class RegisterWindow(QMainWindow): #REGISTRATION WINDOW
    
    registration_complete = pyqtSignal(dict)
    back_to_login = pyqtSignal()
    
    #PROGRAMS IN CCE DEPARTMENT
    PROGRAMS = [
        "BS Computer Science",
        "BS Information Technology",
        "BS Information Systems",
        "BS Library and Information Science",
        "BS EMC - Digital Animation",
        "BS EMC - Game Development",
        "Bachelor of Multimedia Arts"
    ]
    
    YEAR_LEVELS = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        self.setWindowTitle("S.P.E.A.K - Student Registration")
        self.setFixedSize(450, 650)
        self.setStyleSheet(StyleSheet.get_main_window_style())
        
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)
        
        form_layout = QVBoxLayout(scroll_widget)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(30, 20, 30, 20)
        
        self._add_title(form_layout)
        self._add_form_fields(form_layout)
        self._add_buttons(form_layout)
        
        main_layout.addWidget(scroll)
        
    def _add_title(self, layout): #TITLE AND SUBTITLE
        title = QLabel("Student Registration")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        subtitle = QLabel("College of Computing Education")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
    def _add_form_fields(self, layout): #ADD ALL REGISTRATION FORM FIELDS TO THE LAYOUT
        layout.setSpacing(5)
        
        self._add_school_id_field(layout)
        self._add_email_field(layout)
        self._add_name_fields(layout)
        self._add_contact_field(layout)
        self._add_program_year_fields(layout)
        self._add_password_fields(layout)
        
        layout.addSpacing(10)

    def _add_school_id_field(self, layout): #SCHOOL ID INPUT FIELD
        layout.addWidget(QLabel("School ID: <span style='color: red;'>*</span>"))
        self.school_id_input = QLineEdit()
        self.school_id_input.setPlaceholderText("e.g., 560055")
        self.school_id_input.setMinimumHeight(35)
        self.school_id_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.school_id_input)

    def _add_email_field(self, layout): #EMAIL INPUT FIELD
        layout.addWidget(QLabel("School Email: <span style='color: red;'>*</span>"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("name.schoolid@umindanao.edu.ph")
        self.email_input.setMinimumHeight(35)
        self.email_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.email_input)

    def _add_name_fields(self, layout): #NAME INPUT FIELDS
        layout.addWidget(QLabel("First Name: <span style='color: red;'>*</span>"))
        self.fname_input = QLineEdit()
        self.fname_input.setPlaceholderText("Enter first name")
        self.fname_input.setMinimumHeight(35)
        self.fname_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.fname_input)
        
        layout.addWidget(QLabel("Middle Initial:"))
        self.mi_input = QLineEdit()
        self.mi_input.setPlaceholderText("M.I. (optional)")
        self.mi_input.setMinimumHeight(35)
        self.mi_input.setMaxLength(35)
        self.mi_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.mi_input)
        
        layout.addWidget(QLabel("Last Name: <span style='color: red;'>*</span>"))
        self.lname_input = QLineEdit()
        self.lname_input.setPlaceholderText("Enter last name")
        self.lname_input.setMinimumHeight(35)
        self.lname_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.lname_input)

    def _add_contact_field(self, layout): #CONTACT NUMBER INPUT FIELD
        layout.addWidget(QLabel("Contact Number: <span style='color: red;'>*</span>"))
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("09XX-XXX-XXXX")
        self.contact_input.setMinimumHeight(35)
        self.contact_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.contact_input)

    def _add_program_year_fields(self, layout): #PROGRAM AND YR LEVEL DROPDOWN FIELDS
        layout.addWidget(QLabel("Program: <span style='color: red;'>*</span>"))
        self.program_combo = QComboBox()
        self.program_combo.addItems(self.PROGRAMS)
        self.program_combo.setMinimumHeight(35)
        self.program_combo.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.program_combo)
        
        layout.addWidget(QLabel("Year Level: <span style='color: red;'>*</span>"))
        self.year_combo = QComboBox()
        self.year_combo.addItems(self.YEAR_LEVELS)
        self.year_combo.setMinimumHeight(35)
        self.year_combo.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.year_combo)

    def _add_password_fields(self, layout): #PASSWORD AND CONFIRM PASSWORD INPUT FIELDS
        layout.addWidget(QLabel("Password: <span style='color: red;'>*</span>"))
        self.password_input = PasswordInput("Create a password")
        self.password_input.setMinimumHeight(35)
        self.password_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.password_input)
        
        layout.addWidget(QLabel("Confirm Password: <span style='color: red;'>*</span>"))
        self.confirm_password_input = PasswordInput("Re-enter password")
        self.confirm_password_input.setMinimumHeight(35)
        self.confirm_password_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.confirm_password_input)
        
    def _add_buttons(self, layout): #REGISTER AND BACK BUTTONS
        self.register_btn = QPushButton("Register")
        self.register_btn.setMinimumHeight(45)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.clicked.connect(self._on_register_clicked)
        self.register_btn.setStyleSheet(StyleSheet.get_button_style("primary"))
        layout.addWidget(self.register_btn)
        
        layout.addSpacing(10)
        
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        back_label = QLabel("Already have an account?")
        back_layout.addWidget(back_label)
        
        self.back_btn = QPushButton("Back to Login")
        self.back_btn.setFlat(True)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self._on_back_clicked)
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                color: {ColorTheme.GOLDEN_AMBER};
                text-decoration: underline;
                background: transparent;
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {ColorTheme.BTN_PRIMARY_HOVER};
            }}
        """)
        back_layout.addWidget(self.back_btn)
        
        layout.addLayout(back_layout)
        layout.addSpacing(20)
        
    def _on_register_clicked(self):
        student_data = self.get_form_data()
        self.registration_complete.emit(student_data)
        
    def _on_back_clicked(self):
        if self._has_unsaved_changes():
            if self.show_confirmation("Discard Changes?", 
                                     "You have unsaved changes. Go back to login?"):
                self.back_to_login.emit()
        else:
            self.back_to_login.emit()
    
    def get_form_data(self):
        return {
            'school_id': self.school_id_input.text().strip(),
            'email': self.email_input.text().strip(),
            'first_name': self.fname_input.text().strip(),
            'middle_initial': self.mi_input.text().strip(),
            'last_name': self.lname_input.text().strip(),
            'contact_number': self.contact_input.text().strip(),
            'program': self.program_combo.currentText(),
            'year_level': self.year_combo.currentText(),
            'password': self.password_input.text(),
            'confirm_password': self.confirm_password_input.text()
        }
    
    def _has_unsaved_changes(self):
        return any([
            self.school_id_input.text().strip(),
            self.email_input.text().strip(),
            self.fname_input.text().strip(),
            self.lname_input.text().strip(),
            self.contact_input.text().strip(),
            self.password_input.text()
        ])
    
    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)
        
    def show_success(self, title, message):
        QMessageBox.information(self, title, message)
        
    def show_confirmation(self, title, message):
        reply = QMessageBox.question(
            self, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
    
    def clear_fields(self):
        self.school_id_input.clear()
        self.email_input.clear()
        self.fname_input.clear()
        self.mi_input.clear()
        self.lname_input.clear()
        self.contact_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.program_combo.setCurrentIndex(0)
        self.year_combo.setCurrentIndex(0)
        self.school_id_input.setFocus()


class LoginWindow(QMainWindow): #LOGIN WINDOW / FIRST THING YOU SEE IN THE APPLICATION
    login_clicked = pyqtSignal(str, str)
    register_requested = pyqtSignal()
    admin_login_requested = pyqtSignal()
    forgot_password_requested = pyqtSignal()
    
    def _on_admin_clicked(self):
        self.admin_login_requested.emit()
        
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        self.setWindowTitle("S.P.E.A.K - For the people.")
        self.setFixedSize(400, 450)
        self.setStyleSheet(StyleSheet.get_main_window_style())
        
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.addStretch()
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(40, 20, 40, 20)
        
        self._add_title(content_layout)
        self._add_input_fields(content_layout)
        self._add_buttons(content_layout)
        
        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        
    def _add_title(self, layout):
        title = QLabel("Welcome to S.P.E.A.K")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        layout.addSpacing(20)
        
    def _add_input_fields(self, layout): #SCHOOL ID AND PASSWORD INPUT FIELDS
        self.user_label = QLabel("School ID:")
        layout.addWidget(self.user_label)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter School ID...")
        self.user_input.setMinimumHeight(35)
        self.user_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.user_input)
        
        self.pass_label = QLabel("Password:")
        layout.addWidget(self.pass_label)
        
        self.pass_input = PasswordInput("Enter password...")
        self.pass_input.setMinimumHeight(35)
        self.pass_input.returnPressed.connect(self._on_login_clicked)
        self.pass_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.pass_input)
        
        #FORGOT PASSWORD LINK
        forgot_layout = QHBoxLayout()
        forgot_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.forgot_btn = QPushButton("Forgot Password?")
        self.forgot_btn.setFlat(True)
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_btn.clicked.connect(self._on_forgot_password_clicked)
        self.forgot_btn.setStyleSheet(f"""
            QPushButton {{
                color: {ColorTheme.GOLDEN_AMBER};
                text-decoration: underline;
                background: transparent;
                border: none;
                font-size: 11px;
            }}
            QPushButton:hover {{
                color: {ColorTheme.BTN_PRIMARY_HOVER};
            }}
        """)
        forgot_layout.addWidget(self.forgot_btn)
        layout.addLayout(forgot_layout)
        
        layout.addSpacing(10)
        
    def _add_buttons(self, layout):
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.clicked.connect(self._on_login_clicked)
        self.login_btn.setStyleSheet(StyleSheet.get_button_style("primary"))
        layout.addWidget(self.login_btn)
        
        layout.addSpacing(10)
        
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        register_label = QLabel("Don't have an account?")
        register_layout.addWidget(register_label)
        
        self.register_btn = QPushButton("Register")
        self.register_btn.setFlat(True)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.clicked.connect(self._on_register_clicked)
        self.register_btn.setStyleSheet(f"""
            QPushButton {{
                color: {ColorTheme.GOLDEN_AMBER};
                text-decoration: underline;
                background: transparent;
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {ColorTheme.BTN_PRIMARY_HOVER};
            }}
        """)
        register_layout.addWidget(self.register_btn)
        
        layout.addLayout(register_layout)
        
    def _on_login_clicked(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text()
        self.login_clicked.emit(username, password)
        
    def _on_register_clicked(self):
        self.register_requested.emit()
    
    def _on_forgot_password_clicked(self):
        self.forgot_password_requested.emit()
    
    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)
        
    def show_success(self, title, message):
        QMessageBox.information(self, title, message)
    
    def clear_fields(self):
        self.user_input.clear()
        self.pass_input.clear()
        self.user_input.setFocus()


class ForgotPasswordDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        self.setWindowTitle("Reset Password")
        self.setFixedSize(400, 500)
        self.setModal(True)
        self.setStyleSheet(StyleSheet.get_main_window_style())
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(30, 25, 30, 25)
        
        self._add_title(layout)
        self._add_input_fields(layout)
        self._add_buttons(layout)
        
    def _add_title(self, layout):
        title = QLabel("Reset Your Password")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        subtitle = QLabel("Enter your School ID and email to reset")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(15)
        
    def _add_input_fields(self, layout): #ALL INPUT FIELDS FOR PASSWORD RESET
        #SCHOOL ID FIELD
        layout.addWidget(QLabel("School ID:"))
        layout.addSpacing(2)
        self.school_id_input = QLineEdit()
        self.school_id_input.setPlaceholderText("Enter your School ID")
        self.school_id_input.setMinimumHeight(40)
        self.school_id_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.school_id_input)
        layout.addSpacing(5)
        
        #EMAIL FIELD
        layout.addWidget(QLabel("School Email:"))
        layout.addSpacing(2)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("name.schoolid@umindanao.edu.ph")
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.email_input)
        layout.addSpacing(5)
        
        #NEW PASSWORD FIELD WITH TOGGLE
        layout.addWidget(QLabel("New Password:"))
        layout.addSpacing(2)
        self.new_password_input = PasswordInput("Enter new password")
        self.new_password_input.setMinimumHeight(40)
        self.new_password_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.new_password_input)
        layout.addSpacing(5)
        
        #CONFIRM PASSWORD FIELD WITH TOGGLE
        layout.addWidget(QLabel("Confirm Password:"))
        layout.addSpacing(2)
        self.confirm_password_input = PasswordInput("Re-enter new password")
        self.confirm_password_input.setMinimumHeight(40)
        self.confirm_password_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.confirm_password_input)
        
        layout.addSpacing(15)
        
    def _add_buttons(self, layout):
        #RESET BUTTON
        self.reset_btn = QPushButton("Reset Password")
        self.reset_btn.setMinimumHeight(45)
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.accept)
        self.reset_btn.setStyleSheet(StyleSheet.get_button_style("primary"))
        layout.addWidget(self.reset_btn)
        
        layout.addSpacing(12)
        
        #CANCEL BUTTON
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet(StyleSheet.get_button_style("secondary"))
        layout.addWidget(self.cancel_btn)
        
    def get_reset_data(self):
        return {
            'school_id': self.school_id_input.text().strip(),
            'email': self.email_input.text().strip(),
            'new_password': self.new_password_input.text(),
            'confirm_password': self.confirm_password_input.text()
        }