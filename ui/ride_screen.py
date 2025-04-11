# ui/ride_screen.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class RideScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartTaxi - Ride")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: #d1f7c4; font-size: 24px;")

        layout = QVBoxLayout()
        
        self.message = QLabel("✅ Enjoy your ride!", self)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet("color: #2e7d32; font-weight: bold;")

        layout.addWidget(self.message)
        self.setLayout(layout)
