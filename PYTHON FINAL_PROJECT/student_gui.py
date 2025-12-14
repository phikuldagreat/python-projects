#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#GUI FOR STUDENT'S DASHBOARD

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QMessageBox, QHeaderView, QFrame, QLineEdit, QDialog,
    QDialogButtonBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from theme import ColorTheme, StyleSheet


class SubmitComplaintDialog(QDialog): #DIALOG FOR SUBMITTING NEW COMPLAINT
    
    COMPLAINT_CATEGORIES = [
        "Facilities Issue",
        "Equipment Problem",
        "Internet/Network",
        "Classroom Condition",
        "Laboratory Issue",
        "Other"
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Submit New Complaint")
        self.setFixedSize(500, 400)
        self.setStyleSheet(StyleSheet.get_main_window_style())
        self._setup_ui()
        
    def _setup_ui(self): #DIALOG UI
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)
        
        #TITLE
        title = QLabel("Submit a Complaint")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        #CATEGORY
        layout.addWidget(QLabel("Category: <span style='color: red;'>*</span>"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.COMPLAINT_CATEGORIES)
        self.category_combo.setMinimumHeight(35)
        self.category_combo.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.category_combo)
        
        #SUBJECT
        layout.addWidget(QLabel("Subject: <span style='color: red;'>*</span>"))
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Brief description of the issue")
        self.subject_input.setMinimumHeight(35)
        self.subject_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.subject_input)
        
        #LOCATION
        layout.addWidget(QLabel("Location: <span style='color: red;'>*</span>"))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g., Lab 1, Room 301, Building A")
        self.location_input.setMinimumHeight(35)
        self.location_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.location_input)
        
        #DESCRIPTION
        layout.addWidget(QLabel("Detailed Description: <span style='color: red;'>*</span>"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Provide detailed information about your complaint...")
        self.description_input.setMinimumHeight(80)
        self.description_input.setMaximumHeight(80)
        self.description_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.description_input)
        
        #BUTTONS
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def validate_and_accept(self): #INPUT VALIDATOR
        if not self.subject_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a subject.")
            return
        
        if not self.location_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a location.")
            return
        
        if not self.description_input.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a description.")
            return
        
        self.accept()

    def get_complaint_data(self): #GET COMPLAINT DATA FROM INPUT FIELDS
        return {
            'category': self.category_combo.currentText(),
            'subject': self.subject_input.text().strip(),
            'location': self.location_input.text().strip(),
            'description': self.description_input.toPlainText().strip()
        }


class EditComplaintDialog(QDialog): #CLASS FOR EDITING COMPLAINTS
    
    def __init__(self, complaint_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Complaint")
        self.setFixedSize(500, 400)
        self.setStyleSheet(StyleSheet.get_main_window_style())
        self.complaint_data = complaint_data
        self._setup_ui()
        self._populate_data()
        
    def _setup_ui(self): #DIALOG UI
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)
        
        #TITLE
        title = QLabel("Edit Complaint")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        #CATEGORY
        layout.addWidget(QLabel("Category: <span style='color: red;'>*</span>"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(SubmitComplaintDialog.COMPLAINT_CATEGORIES)
        self.category_combo.setMinimumHeight(35)
        self.category_combo.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.category_combo)
        
        #SUBJECT
        layout.addWidget(QLabel("Subject: <span style='color: red;'>*</span>"))
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Brief description of the issue")
        self.subject_input.setMinimumHeight(35)
        self.subject_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.subject_input)
        
        #LOCATION
        layout.addWidget(QLabel("Location: <span style='color: red;'>*</span>"))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g., Lab 1, Room 301, Building A")
        self.location_input.setMinimumHeight(35)
        self.location_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.location_input)
        
        #DESCRIPTION
        layout.addWidget(QLabel("Detailed Description: <span style='color: red;'>*</span>"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Provide detailed information about your complaint...")
        self.description_input.setMinimumHeight(80)
        self.description_input.setMaximumHeight(80)
        self.description_input.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.description_input)
        
        #BUTTONS
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def _populate_data(self): #POPULATE FIELDS WITH EXISTING COMPLAINT DATA
        self.category_combo.setCurrentText(self.complaint_data.get('category', ''))
        self.subject_input.setText(self.complaint_data.get('subject', ''))
        self.location_input.setText(self.complaint_data.get('location', ''))
        self.description_input.setPlainText(self.complaint_data.get('description', ''))
        
    def validate_and_accept(self): #CHECKS IF FIELDS ARE BLANK
        if not self.subject_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a subject.")
            return
        
        if not self.location_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a location.")
            return
        
        if not self.description_input.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a description.")
            return
        
        self.accept()
    
    def get_complaint_data(self): #GET UPDATED COMPLAINT DATA FROM INPUT FIELDS
        return {
            'category': self.category_combo.currentText(),
            'subject': self.subject_input.text().strip(),
            'location': self.location_input.text().strip(),
            'description': self.description_input.toPlainText().strip()
        }


class StudentDashboard(QMainWindow): #STUDENT'S DASHBOARD
    
    logout_requested = pyqtSignal()
    
    def __init__(self, user_data, db):
        super().__init__()
        self.current_user = user_data
        self.db = db
        self._setup_window()
        self._setup_ui()
        self.set_user(user_data)
        self.load_my_complaints()
        
    def _setup_window(self): #MAIN WINDOW PROPERTIES
        self.setWindowTitle("S.P.E.A.K - Student Dashboard")
        self.setStyleSheet(StyleSheet.get_main_window_style())

        
    def _setup_ui(self): #UI COMPONENT CONFIGURATION
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 20)
        
        #HEADER
        self._add_header(main_layout)
        
        #ACTION BUTTONS
        self._add_action_buttons(main_layout)
        
        #COMPLAINTS TABLE
        self._add_complaints_table(main_layout)
        
        #COMPLAINT DETAILS PANEL
        self._add_details_panel(main_layout)
        
        #BOTTOM BUTTONS
        self._add_bottom_buttons(main_layout)
        
    def _add_header(self, layout): #HEADER SECTION
        header_layout = QHBoxLayout()
        
        #USER INFORMATION
        self.user_label = QLabel("Student: Not logged in")
        user_font = QFont()
        user_font.setPointSize(12)
        user_font.setBold(True)
        self.user_label.setFont(user_font)
        header_layout.addWidget(self.user_label)
        
        header_layout.addStretch()
        
        #TITLE
        title = QLabel("My Complaints")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        layout.addLayout(header_layout)
        
    def _add_action_buttons(self, layout): #ADD ACTION BUTTONS
        button_layout = QHBoxLayout()
        
        #SUBMIT COMPLAINT BUTTON
        self.submit_btn = QPushButton("Submit New Complaint")
        self.submit_btn.setMinimumHeight(45)
        self.submit_btn.setMinimumWidth(220)
        self.submit_btn.setFont(QFont("Arial", 11))
        self.submit_btn.clicked.connect(self.submit_complaint)
        self.submit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorTheme.GOLDEN_AMBER};
                color: {ColorTheme.TEXT_PRIMARY};
                font-weight: bold;
                border-radius: 8px;
                border: none;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {ColorTheme.BTN_PRIMARY_HOVER};
            }}
        """)
        button_layout.addWidget(self.submit_btn)
        
        button_layout.addStretch()
        
        #REFRESH BUTTON
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumWidth(150)
        refresh_btn.setMinimumHeight(45)
        refresh_btn.setFont(QFont("Arial", 11))
        refresh_btn.clicked.connect(self.load_my_complaints)
        refresh_btn.setStyleSheet(StyleSheet.get_button_style("primary"))
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
    def _add_complaints_table(self, layout): #ADD COMPLAINTS TABLE
        table_label = QLabel("My Submitted Complaints")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        table_label.setFont(label_font)
        layout.addWidget(table_label)
        
        self.complaints_table = QTableWidget()
        self.complaints_table.setColumnCount(6)
        self.complaints_table.setHorizontalHeaderLabels([
            "ID", "Category", "Subject", "Location", "Status", "Date"
        ])
        
        #COLUMN WIDTHS
        header = self.complaints_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.complaints_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.complaints_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.complaints_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.complaints_table.itemSelectionChanged.connect(self.on_complaint_selected)
        self.complaints_table.setStyleSheet(StyleSheet.get_table_style())
        
        layout.addWidget(self.complaints_table)
        
    def _add_details_panel(self, layout): #ADD COMPLAINT DETAILS PANEL (without buttons)
        details_label = QLabel("Complaint Details")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        details_label.setFont(label_font)
        layout.addWidget(details_label)
        
        details_frame = QFrame()
        details_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        details_frame.setStyleSheet("QFrame { background-color: #f9f9f9; border-radius: 5px; }")
        details_frame.setMaximumHeight(150)
        
        details_layout = QVBoxLayout(details_frame)
        details_layout.setContentsMargins(15, 15, 15, 15)
        
        #DETAILS TEXT AREA
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setPlaceholderText("Select a complaint to view details...")
        self.details_text.setMaximumHeight(120)  # Constrain height
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_frame)
        
        self.selected_complaint_id = None
        self.selected_complaint_status = None
        
    def _add_bottom_buttons(self, layout): #ADD BOTTOM BUTTONS (EDIT, DELETE, LOGOUT)
        bottom_layout = QHBoxLayout()
        
        self._add_edit_delete_buttons(bottom_layout)
        bottom_layout.addStretch()
        self._add_logout_button(bottom_layout)
        
        layout.addLayout(bottom_layout)

    def _add_edit_delete_buttons(self, layout): #ADD EDIT AND DELETE BUTTONS
        left_buttons_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit")  # CREATE FIRST
        self.edit_btn.setEnabled(False)
        self.edit_btn.setMinimumWidth(180)
        self.edit_btn.setMinimumHeight(45)
        self.edit_btn.setFont(QFont("Arial", 11))
        self.edit_btn.clicked.connect(self.edit_complaint)
        self.edit_btn.setStyleSheet(StyleSheet.get_button_style("primary"))  # THEN STYLE
        left_buttons_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Delete")  # CREATE FIRST
        self.delete_btn.setEnabled(False)
        self.delete_btn.setMinimumWidth(180)
        self.delete_btn.setMinimumHeight(45)
        self.delete_btn.setFont(QFont("Arial", 11))
        self.delete_btn.clicked.connect(self.delete_complaint)
        self.delete_btn.setStyleSheet(StyleSheet.get_button_style("danger"))  # THEN STYLE
        left_buttons_layout.addWidget(self.delete_btn)
        
        layout.addLayout(left_buttons_layout)

    def _add_logout_button(self, layout): #ADD LOGOUT BUTTON
        logout_btn = QPushButton("Logout")  # CREATE FIRST
        logout_btn.setMinimumWidth(150)
        logout_btn.setMinimumHeight(45)
        logout_btn.setFont(QFont("Arial", 11))
        logout_btn.clicked.connect(self.logout_requested.emit)
        logout_btn.setStyleSheet(StyleSheet.get_button_style("danger"))  # THEN STYLE
        layout.addWidget(logout_btn)
        
    def set_user(self, user_data): #SET CURRENT USER INFORMATION
        self.current_user = user_data
        full_name = f"{user_data['first_name']} {user_data['last_name']}"
        self.user_label.setText(f"Student: {full_name}")
        
    def submit_complaint(self): #DIALOG OPENS TO SUBMIT NEW COMPLAINT
        dialog = SubmitComplaintDialog(self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            complaint_data = dialog.get_complaint_data()
            
            #ADD STUDENT INFO
            complaint_data['school_id'] = self.current_user['school_id']
            complaint_data['program'] = self.current_user['program']

            print(f"Submitting complaint: {complaint_data}")
            
            #SUBMIT TO DATABASE
            success, message, complaint_id = self.db.submit_complaint(complaint_data)
            
            if success:
                QMessageBox.information(
                    self,
                    "Complaint Submitted",
                    message
                )
                #RE LOAD COMPLAINTS
                self.load_my_complaints()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    message
                )
    
    def edit_complaint(self): #EDIT SELECTED COMPLAINT
        if not self.selected_complaint_id:
            return
        
        #COMPLAINT EDITABILITY CHECKER
        if self.selected_complaint_status == "Resolved":
            QMessageBox.warning(
                self,
                "Cannot Edit",
                "Resolved complaints cannot be edited."
            )
            return
        
        #GET CURRENT COMPLAINT DATA
        row = self.complaints_table.currentRow()
        complaint_data = {
            'category': self.complaints_table.item(row, 1).text(),
            'subject': self.complaints_table.item(row, 2).text(),
            'location': self.complaints_table.item(row, 3).text(),
            'description': self.details_text.toPlainText()
        }
        
        dialog = EditComplaintDialog(complaint_data, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_complaint_data()
            
            #UPDATE IN DATABASE
            success, message = self.db.update_complaint(
                self.selected_complaint_id, 
                updated_data
            )
            
            if success:
                QMessageBox.information(
                    self,
                    "Complaint Updated",
                    message
                )
                #RE LOAD COMPLAINTS
                self.load_my_complaints()
            else:
                QMessageBox.warning(
                    self,
                    "Update Failed",
                    message
                )
    
    def delete_complaint(self): #DELETE SELECTED COMPLAINT
        if not self.selected_complaint_id:
            return
        
        #CHECK IF COMPLAINT CAN BE DELETED
        if self.selected_complaint_status in ["In Progress", "Resolved"]:
            QMessageBox.warning(
                self,
                "Cannot Delete",
                f"{self.selected_complaint_status} complaints cannot be deleted."
            )
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete complaint #{self.selected_complaint_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            #DELETE FROM DATABASE
            success, message = self.db.delete_complaint(self.selected_complaint_id)
            
            if success:
                QMessageBox.information(
                    self,
                    "Complaint Deleted",
                    message
                )
                #RE LOAD COMPLAINTS
                self.load_my_complaints()
            else:
                QMessageBox.warning(
                    self,
                    "Delete Failed",
                    message
                )
    
    def load_my_complaints(self): #LOAD STUDENT COMPLAINTS FROM DATABASE
        if not self.current_user:
            return
        
        #GET COMPLAINTS FROM DATABASE
        complaints = self.db.get_student_complaints(self.current_user['school_id'])
        
        formatted_complaints = [
            (
                complaint['id'],
                complaint['category'],
                complaint['subject'],
                complaint['location'],
                complaint['status'],
                complaint['date'],
                complaint['description']
            )
            for complaint in complaints
        ]
        
        self.display_complaints(formatted_complaints)
        
    def display_complaints(self, complaints): #DISPLAY COMPLAINTS IN TABLE
        self.complaints_table.setRowCount(len(complaints))
        self.all_complaints = complaints
        
        for row, complaint in enumerate(complaints):
            for col in range(6):
                item = QTableWidgetItem(str(complaint[col]))
                
                #COLOR CODE
                if col == 4:  # Status column
                    if complaint[col] == "Pending":
                        item.setForeground(QColor(ColorTheme.STATUS_PENDING))
                    elif complaint[col] == "In Progress":
                        item.setForeground(QColor(ColorTheme.STATUS_IN_PROGRESS))
                    elif complaint[col] == "Resolved":
                        item.setForeground(QColor(ColorTheme.STATUS_RESOLVED))
                
                self.complaints_table.setItem(row, col, item)
        
    def on_complaint_selected(self): #HANDLES COMPLAINT SELECTION FROM TABLE
        selected = self.complaints_table.selectedItems()
        if not selected:
            self.details_text.clear()
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            return
        
        row = selected[0].row()
        complaint = self.all_complaints[row]
        
        self.selected_complaint_id = complaint[0]
        self.selected_complaint_status = complaint[4]
        
        #DISPLAY DETAILS
        details = f"""Category: {complaint[1]}
                    Subject: {complaint[2]}
                    Location: {complaint[3]}
                    Status: {complaint[4]}
                    Date Submitted: {complaint[5]}
                    Description: {complaint[6]}
                    """
        
        self.details_text.setText(details.strip())
        
        #ENABLE/DISABLE EDIT & DELETE BUTTONS BASED ON STATUS
        if complaint[4] == "Pending":
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        elif complaint[4] == "In Progress":
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
        else:
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
