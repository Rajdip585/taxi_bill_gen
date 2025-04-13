# # ui/face_scan_screen.py

# from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
# from modules.face_recognition_handler import FaceRecognizer
# from ui.pickup_destination_screen import PickupDestinationScreen
# from PyQt5.QtGui import QPixmap, QFont
# from PyQt5.QtCore import Qt

# class FaceScanScreen(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("SmartTaxi - Face Scan")
#         self.setStyleSheet("font-size: 16px;")

#         # 💀 UI Elements
#         self.label = QLabel("Welcome to SmartTaxi 🚖\nClick below to scan your face")
#         self.button = QPushButton("Scan Face")
#         self.button.clicked.connect(self.scan_face)

#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.button)
#         self.setLayout(layout)

#         # 🎭 Face Handler
#         self.face_handler = FaceRecognizer()

#     def scan_face(self):
#         name = self.face_handler.recognize_face()

#         if name and name != "Unknown":
#             QMessageBox.information(self, "Recognized", f"Hi {name}! You’re all set.")
#             # TODO: navigate to next screen (pickup/destination screen)
#             self.new_window = PickupDestinationScreen(name)
#             self.new_window.show()
#         else:
#             QMessageBox.warning(self, "Failed", "Face not recognized. Please try again.")

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox, QSpacerItem, QSizePolicy
from modules.face_recognition_handler import FaceRecognizer
from ui.pickup_destination_screen import PickupDestinationScreen
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class FaceScanScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SmartTaxi - Face Scan")
        self.setFixedSize(400, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f8fa;
                font-family: 'Segoe UI', sans-serif;
                color: #333;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QVBoxLayout {
                margin: 20px;
            }
        """)

        # UI Elements
        self.label = QLabel("Welcome to SmartTaxi 🚖\nClick below to scan your face", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Segoe UI", 16))

        self.button = QPushButton("Scan Face", self)
        self.button.clicked.connect(self.scan_face)

        # Spacer for vertical centering
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addItem(spacer)  # Add spacer to center the button
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Face Handler
        self.face_handler = FaceRecognizer()

    def scan_face(self):
        name = self.face_handler.recognize_face()

        if name and name != "Unknown":
            # Face recognized
            QMessageBox.information(self, "Face Recognized", f"Hi {name}! You’re all set.")
            # Navigate to next screen (pickup/destination screen)
            self.new_window = PickupDestinationScreen(name)
            self.new_window.show()
            self.close()  # Close the face scan screen after moving to the next one
        else:
            # Face not recognized
            QMessageBox.warning(self, "Failed", "Face not recognized. Please try again.")
