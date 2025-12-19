#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#ADMIN'S DASHBOARD GUI

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QTextEdit, QMessageBox, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from theme import ColorTheme, StyleSheet


class AdminDashboard(QMainWindow): #ADMIN DASHBOARD TO MANAGE AND VIEW COMPLAINTS
    
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_admin = None
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        self.setWindowTitle("S.P.E.A.K - Admin Dashboard")
        self.setStyleSheet(StyleSheet.get_main_window_style())
        
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 20)
        
        self._add_header(main_layout)
        self._add_filters(main_layout)
        self._add_complaints_table(main_layout)
        self._add_details_panel(main_layout)
        self._add_bottom_buttons(main_layout)
        
    def _add_header(self, layout):
        header_layout = QHBoxLayout()
        
        self.admin_label = QLabel("Admin: Not logged in")
        admin_font = QFont()
        admin_font.setPointSize(12)
        admin_font.setBold(True)
        self.admin_label.setFont(admin_font)
        header_layout.addWidget(self.admin_label)
        
        header_layout.addStretch()
        
        title = QLabel("Dashboard - Admin")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        layout.addLayout(header_layout)
        
    def _add_filters(self, layout): #ADD FILTER CONTROLS TO THE LAYOUT
        filter_frame = self._create_filter_frame()
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        
        self._add_program_filter(filter_layout)
        filter_layout.addSpacing(30)
        self._add_status_filter(filter_layout)
        filter_layout.addStretch()
        self._add_refresh_button(filter_layout)
        filter_layout.addSpacing(10)
        self._add_login_history_button(filter_layout)
        
        layout.addWidget(filter_frame)

    def _create_filter_frame(self): #CREATE + STYLE FILTER FRAME CONTAINER
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorTheme.BG_PANEL};
                border: 2px solid {ColorTheme.BORDER_LIGHT};
                border-radius: 8px;
            }}
        """)
        return filter_frame

    def _add_program_filter(self, layout): #PROGRAM FILTER DROPDOWN
        filter_program_label = QLabel("Filter by Program:")
        filter_program_label.setFont(QFont("Arial", 12))
        layout.addWidget(filter_program_label)
        
        self.program_filter = QComboBox()
        self.program_filter.addItems([
            "All Programs",
            "BS Computer Science",
            "BS Information Technology",
            "BS Information Systems",
            "BS Library and Information Science",
            "BS EMC - Digital Animation",
            "BS EMC - Game Development",
            "Bachelor of Multimedia Arts"
        ])
        self.program_filter.currentTextChanged.connect(self.filter_complaints)
        self.program_filter.setMinimumWidth(400)
        self.program_filter.setMinimumHeight(40)
        self.program_filter.setFont(QFont("Arial", 11))
        self.program_filter.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.program_filter)

    def _add_status_filter(self, layout): #STATUS FILTER DROPDOWN
        filter_status_label = QLabel("Filter by Status:")
        filter_status_label.setFont(QFont("Arial", 12))
        layout.addWidget(filter_status_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "All Status",
            "Pending",
            "In Progress",
            "Resolved"
        ])
        self.status_filter.currentTextChanged.connect(self.filter_complaints)
        self.status_filter.setMinimumWidth(200)
        self.status_filter.setMinimumHeight(40)
        self.status_filter.setFont(QFont("Arial", 11))
        self.status_filter.setStyleSheet(StyleSheet.get_input_style())
        layout.addWidget(self.status_filter)
    
    def _add_refresh_button(self, layout): #REFRESH BUTTON
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumWidth(150)
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setFont(QFont("Arial", 11))
        refresh_btn.clicked.connect(self.load_complaints)
        refresh_btn.setStyleSheet(StyleSheet.get_button_style("primary"))
        layout.addWidget(refresh_btn)
        
    def _add_complaints_table(self, layout): #COMPLAINTS TABLE
        
        self.complaints_table = QTableWidget()
        self.complaints_table.setColumnCount(6)
        self.complaints_table.setHorizontalHeaderLabels([
            "ID", "Student ID", "Program", "Complaint", "Status", "Date"
        ])
        
        header = self.complaints_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.complaints_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.complaints_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.complaints_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.complaints_table.itemSelectionChanged.connect(self.on_complaint_selected)
        self.complaints_table.setStyleSheet(StyleSheet.get_table_style())
        
        layout.addWidget(self.complaints_table)
        
    def _add_details_panel(self, layout): #COMPLAINT DETAILS PANEL
        details_label = QLabel("Complaint Details")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        details_label.setFont(label_font)
        layout.addWidget(details_label)
        
        details_frame = QFrame()
        details_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        details_frame.setMaximumHeight(180)
        details_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorTheme.BG_CARD};
                border: 2px solid {ColorTheme.BORDER_LIGHT};
                border-radius: 8px;
            }}
        """)  # THEN STYLE
        
        details_layout = QVBoxLayout(details_frame)
        details_layout.setContentsMargins(15, 15, 15, 15)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setPlaceholderText("Select a complaint to view details...")
        self.details_text.setMaximumHeight(150)
        self.details_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ColorTheme.WHITE};
                border: none;
                color: {ColorTheme.TEXT_PRIMARY};
            }}
        """)
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_frame)
        
        self.selected_complaint_id = None
        
    def _add_bottom_buttons(self, layout): #BOTTOM BUTTONS LAYOUT
        bottom_layout = QHBoxLayout()
        
        left_buttons_layout = QHBoxLayout()
        
        self.in_progress_btn = QPushButton("Mark In Progress")
        self.in_progress_btn.setEnabled(False)
        self.in_progress_btn.setMinimumWidth(180)
        self.in_progress_btn.setMinimumHeight(45)
        self.in_progress_btn.setFont(QFont("Arial", 11))
        self.in_progress_btn.clicked.connect(lambda: self.update_status("In Progress"))
        self.in_progress_btn.setStyleSheet(StyleSheet.get_button_style("secondary"))
        left_buttons_layout.addWidget(self.in_progress_btn)
        
        self.resolve_btn = QPushButton("Mark as Resolved")
        self.resolve_btn.setEnabled(False)
        self.resolve_btn.setMinimumWidth(180)
        self.resolve_btn.setMinimumHeight(45)
        self.resolve_btn.setFont(QFont("Arial", 11))
        self.resolve_btn.clicked.connect(lambda: self.update_status("Resolved"))
        self.resolve_btn.setStyleSheet(StyleSheet.get_button_style("success"))
        left_buttons_layout.addWidget(self.resolve_btn)
        
        bottom_layout.addLayout(left_buttons_layout)
        bottom_layout.addStretch()
        
        logout_btn = QPushButton("Logout")  # CREATE FIRST
        logout_btn.setMinimumWidth(150)
        logout_btn.setMinimumHeight(45)
        logout_btn.setFont(QFont("Arial", 11))
        logout_btn.clicked.connect(self.logout_requested.emit)
        logout_btn.setStyleSheet(StyleSheet.get_button_style("danger"))
        bottom_layout.addWidget(logout_btn)
        
        layout.addLayout(bottom_layout)
        
    def set_admin(self, admin_name):
        self.current_admin = admin_name
        self.admin_label.setText(f"Admin: {admin_name}")
        
    def load_complaints(self):
        from database import Database
        from config import DB_CONFIG
        
        print(f"DB_CONFIG: {DB_CONFIG}")
        db = Database(**DB_CONFIG)
        if db.connect():
            complaints_data = db.get_all_complaints()
            print(f"Got {len(complaints_data)} complaints")
            print(f"Raw complaints from DB: {complaints_data}")
            db.close()
            
            complaints = []
            for c in complaints_data:
                complaints.append((
                    c['id'],
                    c['school_id'],
                    c['program'],
                    c['complaint'],
                    c['status'],
                    c['date']
                ))
            
            self.all_complaints_full = complaints_data
            self.all_complaints = complaints
            self.display_complaints(complaints)
        else:
            print("Failed to connect to database!")
            self.all_complaints = []
            self.display_complaints([])
            
    def display_complaints(self, complaints): #DISPLAY COMPLAINTS IN THE TABLE
        self.complaints_table.setRowCount(len(complaints))
        
        for row, complaint in enumerate(complaints):
            for col, data in enumerate(complaint):
                item = QTableWidgetItem(str(data))
                
                #STATUS COLOR CODES
                if col == 4:  # STATUS COLUMN
                    if data == "Pending":
                        item.setForeground(QColor(ColorTheme.STATUS_PENDING))
                    elif data == "In Progress":
                        item.setForeground(QColor(ColorTheme.STATUS_IN_PROGRESS))
                    elif data == "Resolved":
                        item.setForeground(QColor(ColorTheme.STATUS_RESOLVED))
                
                self.complaints_table.setItem(row, col, item)
        
    def filter_complaints(self): #FILTER COMPLAINTS BASED ON SELECTED FILTERS
        program = self.program_filter.currentText()
        status = self.status_filter.currentText()
        
        filtered = self.all_complaints
        
        #FILTER BY PROGRAM
        if program != "All Programs":
            filtered = [c for c in filtered if c[2] == program]
        
        #FILTER BY STATUS
        if status != "All Status":
            filtered = [c for c in filtered if c[4] == status]
        
        self.display_complaints(filtered)
        
    def on_complaint_selected(self): #HANDLE COMPLAINT SELECTION
        selected = self.complaints_table.selectedItems()
        if not selected:
            self.details_text.clear()
            self.in_progress_btn.setEnabled(False)
            self.resolve_btn.setEnabled(False)
            return
        
        row = selected[0].row()
        complaint_id = self.complaints_table.item(row, 0).text()
        
        complaint = None
        for c in self.all_complaints_full:
            if str(c['id']) == complaint_id:
                complaint = c
                break
        
        if not complaint:
            return
        
        self.selected_complaint_id = complaint_id
        
        details = f"""
                Complaint ID: {complaint['id']}
                Student ID: {complaint['school_id']}
                Program: {complaint['program']}
                Status: {complaint['status']}
                Date Submitted: {complaint['date']}
                Category: {complaint['category']}
                Location: {complaint['location']}
                Complaint: {complaint['complaint']}
                Description: {complaint['description']}
                """
        
        self.details_text.setText(details.strip())
        
        status = complaint['status']
        if status == "Resolved":
            self.in_progress_btn.setEnabled(False)
            self.resolve_btn.setEnabled(False)
        elif status == "In Progress":
            self.in_progress_btn.setEnabled(False)
            self.resolve_btn.setEnabled(True)
        else:
            self.in_progress_btn.setEnabled(True)
            self.resolve_btn.setEnabled(True)
        
    def update_status(self, new_status): #UPDATE COMPLAINT STATUS
        if not self.selected_complaint_id:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Status Change",
            f"Mark complaint #{self.selected_complaint_id} as {new_status}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from database import Database
            from config import DB_CONFIG
            
            db = Database(**DB_CONFIG)
            if db.connect():
                success, message = db.update_complaint_status(
                    self.selected_complaint_id, 
                    new_status
                )
                db.close()
                
                if success:
                    QMessageBox.information(self, "Status Updated", message)
                    self.load_complaints()
                else:
                    QMessageBox.warning(self, "Update Failed", message)

    def _add_login_history_button(self, layout): #ADD LOGIN HISTORY BUTTON TO FILTERS
        login_history_btn = QPushButton("View Login History")
        login_history_btn.setMinimumWidth(180)
        login_history_btn.setMinimumHeight(40)
        login_history_btn.setFont(QFont("Arial", 11))
        login_history_btn.clicked.connect(self.show_login_history_dialog)
        login_history_btn.setStyleSheet(StyleSheet.get_button_style("secondary"))
        layout.addWidget(login_history_btn)

    def show_login_history_dialog(self): #SHOW LOGIN HISTORY IN A DIALOG
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Student Login History")
        dialog.setMinimumWidth(700)
        dialog.setMinimumHeight(500)
        dialog.setStyleSheet(StyleSheet.get_main_window_style())
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        #SEARCH INPUT
        search_layout = QHBoxLayout()
        search_label = QLabel("Enter Student ID:")
        search_label.setFont(QFont("Arial", 11))
        search_layout.addWidget(search_label)
        
        student_id_input = QLineEdit()
        student_id_input.setPlaceholderText("e.g., 560055")
        student_id_input.setMinimumHeight(35)
        student_id_input.setFont(QFont("Arial", 11))
        student_id_input.setStyleSheet(StyleSheet.get_input_style())
        search_layout.addWidget(student_id_input)
        
        search_btn = QPushButton("Search")
        search_btn.setMinimumWidth(100)
        search_btn.setMinimumHeight(35)
        search_btn.setFont(QFont("Arial", 11))
        search_btn.setStyleSheet(StyleSheet.get_button_style("primary"))
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)
        
        #RESULTS TABLE
        results_label = QLabel("Login History")
        results_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(results_label)
        
        history_table = QTableWidget()
        history_table.setColumnCount(3)
        history_table.setHorizontalHeaderLabels(["Login Time", "IP Address", "Student Info"])
        
        header = history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        history_table.setStyleSheet(StyleSheet.get_table_style())
        layout.addWidget(history_table)

        #SEARCH FUNCTION (nested inside show_login_history_dialog)
        def search_history():
            student_id = student_id_input.text().strip()
            if not student_id:
                QMessageBox.warning(dialog, "Input Required", "Please enter a Student ID.")
                return
            
            from database import Database
            from config import DB_CONFIG
            
            db = Database(**DB_CONFIG)
            if db.connect():
                #GET STUDENT INFO
                db.cursor.execute(
                    "SELECT id, first_name, last_name, program FROM students WHERE school_id = %s",
                    (student_id,)
                )
                student = db.cursor.fetchone()
                
                if not student:
                    QMessageBox.warning(dialog, "Not Found", f"No student found with ID: {student_id}")
                    db.close()
                    return
                
                #GET LOGIN HISTORY
                history = db.get_login_history(student['id'], limit=50)
                db.close()
                
                #DISPLAY RESULTS
                history_table.setRowCount(len(history))
                student_info = f"{student['first_name']} {student['last_name']} - {student['program']}"
                
                for row, login in enumerate(history):
                    history_table.setItem(row, 0, QTableWidgetItem(login['login_time']))
                    history_table.setItem(row, 1, QTableWidgetItem(login['ip_address'] or "N/A"))
                    history_table.setItem(row, 2, QTableWidgetItem(student_info))
                
                results_label.setText(f"Login History - {len(history)} records found")
            else:
                QMessageBox.critical(dialog, "Database Error", "Could not connect to database.")
        
        # Connect the search button to the nested function
        search_btn.clicked.connect(search_history)
        student_id_input.returnPressed.connect(search_history)
        
        #CLOSE BUTTON
        close_btn = QPushButton("Close")
        close_btn.setMinimumWidth(120)
        close_btn.setMinimumHeight(40)
        close_btn.setFont(QFont("Arial", 11))
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet(StyleSheet.get_button_style("danger"))
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        dialog.exec()