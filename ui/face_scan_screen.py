# ui/face_scan_screen.py

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox
from modules.face_recognition_handler import FaceRecognizer
from ui.pickup_destination_screen import PickupDestinationScreen

class FaceScanScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SmartTaxi - Face Scan")
        self.setStyleSheet("font-size: 16px;")

        # 💀 UI Elements
        self.label = QLabel("Welcome to SmartTaxi 🚖\nClick below to scan your face")
        self.button = QPushButton("Scan Face")
        self.button.clicked.connect(self.scan_face)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 🎭 Face Handler
        self.face_handler = FaceRecognizer()

    def scan_face(self):
        name = self.face_handler.recognize_face()

        if name and name != "Unknown":
            QMessageBox.information(self, "Recognized", f"Hi {name}! You’re all set.")
            # TODO: navigate to next screen (pickup/destination screen)
            self.new_window = PickupDestinationScreen(name)
            self.new_window.show()
        else:
            QMessageBox.warning(self, "Failed", "Face not recognized. Please try again.")
