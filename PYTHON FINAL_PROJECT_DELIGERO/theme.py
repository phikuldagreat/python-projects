#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#COLOR THEME FOR THE WHOLE APPLICATION

class ColorTheme:

    #PRIMARY COLORS
    PASTEL_YELLOW = "#FFF9E6"
    WARM_YELLOW = "#FFE8A3"
    GOLDEN_AMBER = "#FFB84D"
    
    #TEXT COLORS
    TEXT_PRIMARY = "#3A3A3A"
    TEXT_SECONDARY = "#5A6C7D"
    TEXT_HEADER = "#4A5568"
    
    #BG COLORS
    BG_MAIN = "#FFF9E6"
    BG_CARD = "#FFF8E1"
    BG_PANEL = "#FFFBF0"
    BG_SIDEBAR = "#FFE8A3"
    
    #BTN COLORS
    BTN_PRIMARY = "#FFB84D"
    BTN_PRIMARY_HOVER = "#FFA630"
    BTN_SECONDARY = "#5A6C7D"
    BTN_SECONDARY_HOVER = "#4A5568"
    BTN_SUCCESS = "#7BA05B"
    BTN_SUCCESS_HOVER = "#6A8F4A"
    BTN_DANGER = "#D97373"
    BTN_DANGER_HOVER = "#C85F5F"
    
    #STATUS COLORS
    STATUS_PENDING = "#E67E50"
    STATUS_IN_PROGRESS = "#52A69C"
    STATUS_RESOLVED = "#7BA05B"
    
    #ACCENT COLORS
    ACCENT_TEAL = "#4A9B8E"
    ACCENT_BLUE = "#5A6C7D"
    
    #BORDER & DIVIDER COLORS
    BORDER_LIGHT = "#FFE8A3"
    BORDER_MEDIUM = "#FFD480"
    DIVIDER = "#F5E6C8"
    
    #WHITE AND NEUTRALS
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F5F5F5"


class StyleSheet: #STYLE SHEET TEMPLATES FOR DIFFERENT WIDGETS
    
    @staticmethod
    def get_main_window_style():
        return f"""
            QMainWindow {{
                background-color: {ColorTheme.BG_MAIN};
            }}
            QWidget {{
                background-color: {ColorTheme.BG_MAIN};
                color: {ColorTheme.TEXT_PRIMARY};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """
    
    @staticmethod
    def get_button_style(button_type="primary"):
        if button_type == "primary":
            return f"""
                QPushButton {{
                    background-color: {ColorTheme.BTN_PRIMARY};
                    color: {ColorTheme.TEXT_PRIMARY};
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {ColorTheme.BTN_PRIMARY_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: #E69520;
                }}
                QPushButton:disabled {{
                    background-color: {ColorTheme.LIGHT_GRAY};
                    color: {ColorTheme.TEXT_SECONDARY};
                }}
            """
        elif button_type == "success":
            return f"""
                QPushButton {{
                    background-color: {ColorTheme.BTN_SUCCESS};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {ColorTheme.BTN_SUCCESS_HOVER};
                }}
                QPushButton:disabled {{
                    background-color: {ColorTheme.LIGHT_GRAY};
                    color: {ColorTheme.TEXT_SECONDARY};
                }}
            """
        elif button_type == "danger":
            return f"""
                QPushButton {{
                    background-color: {ColorTheme.BTN_DANGER};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {ColorTheme.BTN_DANGER_HOVER};
                }}
                QPushButton:disabled {{
                    background-color: {ColorTheme.LIGHT_GRAY};
                    color: {ColorTheme.TEXT_SECONDARY};
                }}
            """
        else:  #SECONDARY BUTTON
            return f"""
                QPushButton {{
                    background-color: {ColorTheme.BTN_SECONDARY};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: {ColorTheme.BTN_SECONDARY_HOVER};
                }}
            """
    
    @staticmethod
    def get_input_style():
        return f"""
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {ColorTheme.WHITE};
                border: 2px solid {ColorTheme.BORDER_LIGHT};
                border-radius: 6px;
                padding: 8px 12px;
                color: {ColorTheme.TEXT_PRIMARY};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 2px solid {ColorTheme.GOLDEN_AMBER};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {ColorTheme.TEXT_SECONDARY};
            }}
        """
    
    @staticmethod
    def get_table_style():
        return f"""
            QTableWidget {{
                background-color: {ColorTheme.WHITE};
                border: 2px solid {ColorTheme.BORDER_LIGHT};
                border-radius: 8px;
                gridline-color: {ColorTheme.DIVIDER};
            }}
            QTableWidget::item {{
                padding: 8px;
                color: {ColorTheme.TEXT_PRIMARY};
            }}
            QTableWidget::item:selected {{
                background-color: {ColorTheme.WARM_YELLOW};
                color: {ColorTheme.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {ColorTheme.GOLDEN_AMBER};
                color: {ColorTheme.TEXT_PRIMARY};
                padding: 10px;
                border: none;
                border-right: 1px solid {ColorTheme.BORDER_MEDIUM};
                font-weight: bold;
            }}
        """
    
    @staticmethod
    def get_frame_style():
        return f"""
            QFrame {{
                background-color: {ColorTheme.BG_CARD};
                border: 2px solid {ColorTheme.BORDER_LIGHT};
                border-radius: 8px;
            }}
        """