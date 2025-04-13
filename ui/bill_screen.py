# from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
# from PyQt5.QtGui import QPixmap, QFont
# from PyQt5.QtCore import Qt
# import os

# class BillScreen(QWidget):
#     def __init__(self, bill_data):
#         super().__init__()
#         self.setWindowTitle("Your SmartTaxi Bill 🧾")
#         self.setFixedSize(500, 600)

#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         # 🖼️ Add template image
#         image_path = os.path.join(os.path.dirname(__file__), 'assets', 'bill_template.png')
#         pixmap = QPixmap(image_path).scaled(450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         image_label = QLabel()
#         image_label.setPixmap(pixmap)
#         image_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(image_label)

#         # 📝 Overlay text details
#         self.add_detail(f"Name: {bill_data['username']}")
#         self.add_detail(f"Pickup: {bill_data['pickup']}")
#         self.add_detail(f"Destination: {bill_data['destination']}")
#         self.add_detail(f"Distance: {bill_data['distance']} km")
#         self.add_detail(f"Amount: ₹{bill_data['amount']}")

#     def add_detail(self, text):
#         label = QLabel(text)
#         label.setFont(QFont("Arial", 14))
#         label.setStyleSheet("color: #333; padding: 4px;")
#         label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(label)

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os

class BillScreen(QWidget):
    def __init__(self, bill_data):
        super().__init__()
        self.setWindowTitle("Your SmartTaxi Bill 🧾")
        self.setFixedSize(500, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 🖼️ Add template image
        image_path = os.path.join(os.path.dirname(__file__), 'assets', 'bill_template.png')
        pixmap = QPixmap(image_path).scaled(450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label)

        # 🏷️ Add bill heading, aligned to the left
        heading = QLabel("SmartTaxi Bill")
        heading.setFont(QFont("Arial", 18, QFont.Bold))
        heading.setStyleSheet("color: #2c3e50; margin-bottom: 10px; padding-left: 10px;")
        heading.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(heading)

        # 📝 Use QLineEdit for displaying details, pre-filled and non-editable
        self.add_detail("Name", bill_data['username'])
        self.add_detail("Pickup", bill_data['pickup'])
        self.add_detail("Destination", bill_data['destination'])
        self.add_detail("Distance", f"{bill_data['distance']} km")
        self.add_detail("Amount", f"₹{bill_data['amount']}")

        # 🛑 Add some padding to the layout for better visual spacing
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.ok_button.clicked.connect(self.close_bill)
        self.layout.addWidget(self.ok_button)
        
    def add_detail(self, label_text, value):
        # Create a label and input field for each detail
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("color: #34495e; padding-top: 10px; padding-bottom: 5px;")
        label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(label)

        # Create a QLineEdit input field with better styling and padding
        input_field = QLineEdit(value)
        input_field.setFont(QFont("Arial", 12))
        input_field.setStyleSheet("""
            color: #2c3e50;
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
        """)
        input_field.setReadOnly(True)  # Make the input field non-editable
        input_field.setFixedHeight(40)  # Set a fixed height for consistency
        self.layout.addWidget(input_field)

        # 🏆 Add some spacing between each detail block
        self.layout.addSpacing(10)
        
    def close_bill(self):
        # Close the bill screen when the OK button is clicked
        self.close()