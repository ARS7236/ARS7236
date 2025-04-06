import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QVBoxLayout, QPushButton, QLabel, QWidget, QListWidget, QComboBox, QToolBar, QMainWindow
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

# Paths for Resource Hacker and Template DLL
RESOURCE_HACKER_PATH = r"C:\\Program Files (x86)\\Resource Hacker\\ResourceHacker.exe"
TEMPLATE_DLL_PATH = r"C:\Users\ARS7236\Desktop\Folders\projects\resource_gighack\default.template.dll"

class ResourceGighack(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resource Gighack")
        self.setGeometry(100, 100, 600, 400)
        
        self.current_theme = "light"
        self.set_theme(self.current_theme)
        
        self.init_ui()

    def init_ui(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        self.blank_file_action = self.toolbar.addAction("Blank File")
        self.blank_file_action.triggered.connect(self.create_blank_file)

        self.open_file_action = self.toolbar.addAction("Open")
        self.open_file_action.triggered.connect(self.open_file)
        
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel("Choose Output Folder")
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        layout.addWidget(self.list_widget)

        self.select_button = QPushButton("Choose Output Folder")
        self.select_button.setFont(QFont("Segoe UI", 10))
        self.select_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #0078D4; color: white;")
        self.select_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.select_button)

        self.icon_button = QPushButton("Choose Icon(s)")
        self.icon_button.setFont(QFont("Segoe UI", 10))
        self.icon_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #FFA500; color: white;")
        self.icon_button.clicked.connect(self.select_icons)
        layout.addWidget(self.icon_button)

        self.create_button = QPushButton("Create DLL")
        self.create_button.setFont(QFont("Segoe UI", 10))
        self.create_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #107C10; color: white;")
        self.create_button.clicked.connect(self.create_dll)
        layout.addWidget(self.create_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setFont(QFont("Segoe UI", 10))
        self.settings_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #5A5A5A; color: white;")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.output_folder = ""
        self.selected_icons = []

    def create_blank_file(self):
        self.list_widget.clear()
        QMessageBox.information(self, "New File", "Created a new blank file.")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Executable Files (*.exe *.dll *.rc)")
        if file_path:
            QMessageBox.information(self, "File Opened", f"Opened: {file_path}")

    def open_settings(self):
        self.settings_window = QWidget()
        self.settings_window.setWindowTitle("Settings")
        self.settings_window.setGeometry(150, 150, 300, 200)
        
        layout = QVBoxLayout()
        
        self.theme_label = QLabel("Select Theme")
        self.theme_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.theme_label)
        
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Light", "Dark"])
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        layout.addWidget(self.theme_selector)
        
        self.settings_window.setLayout(layout)
        self.settings_window.show()

    def change_theme(self, theme):
        self.current_theme = theme.lower()
        self.set_theme(self.current_theme)

    def set_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet("background-color: #2D2D30; color: white;")
        else:
            self.setStyleSheet("background-color: #f3f3f3; color: black;")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.list_widget.clear()
            self.list_widget.addItem(self.output_folder)

    def select_icons(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Icon Files", "", "Icon Files (*.ico)")
        if files:
            self.selected_icons = files
            self.list_widget.clear()
            self.list_widget.addItems(self.selected_icons)

    def create_dll(self):
        if not self.output_folder:
            QMessageBox.warning(self, "Warning", "No output folder selected.")
            return
        if not self.selected_icons:
            QMessageBox.warning(self, "Warning", "No icons selected.")
            return

        output_dll = os.path.join(self.output_folder, "output.dll")
        
        # Copy the template DLL to output location to preserve original file
        subprocess.run(["copy", TEMPLATE_DLL_PATH, output_dll], shell=True)
        
        for idx, icon in enumerate(self.selected_icons, start=1):
            command = [
                RESOURCE_HACKER_PATH,
                "-open", output_dll,  # Now modifying output DLL instead of overwriting
                "-save", output_dll,
                "-action", "add",
                "-res", icon,
                "-mask", f"ICONGROUP,{idx},0"
            ]
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Failed to add icon {icon}: {e}")
                return

        QMessageBox.information(self, "Success", f"DLL created at {output_dll}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResourceGighack()
    window.show()
    sys.exit(app.exec_())
