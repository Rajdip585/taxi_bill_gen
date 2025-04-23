from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class RideScreen(QWidget):
    def __init__(self, utr_number="123456789012"):  # You can pass real UTR number here
        super().__init__()
        self.setWindowTitle("SmartTaxi - Ride")
        self.setFixedSize(400, 250)
        self.setStyleSheet("background-color: #d1f7c4; font-size: 18px;")

        layout = QVBoxLayout()

        # 🧾 Payment success message
        thank_you = QLabel("🎉 Thanks for your payment!", self)
        thank_you.setAlignment(Qt.AlignCenter)
        thank_you.setStyleSheet("color: #2e7d32; font-weight: bold; font-size: 20px;")
        layout.addWidget(thank_you)

        # 📄 UTR number
        utr_label = QLabel(f"UTR No: {utr_number}", self)
        utr_label.setAlignment(Qt.AlignCenter)
        utr_label.setStyleSheet("color: #000000; font-size: 16px; margin-top: 10px;")
        layout.addWidget(utr_label)

        # 🚕 Ride message
        ride_msg = QLabel("✅ Enjoy your ride!", self)
        ride_msg.setAlignment(Qt.AlignCenter)
        ride_msg.setStyleSheet("color: #2e7d32; font-weight: bold; font-size: 18px; margin-top: 20px;")
        layout.addWidget(ride_msg)

        self.setLayout(layout)
