from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, QTimer
from modules import db_handler
import qrcode
import uuid
import os
import time
import requests  # Make sure this is installed: pip install requests
from ui.ride_screen import RideScreen

def generate_qr_code(data, save_dir='assets/qr'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = f"qr_{uuid.uuid4().hex[:8]}.png"
    full_path = os.path.join(save_dir, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(full_path)
    return full_path

class BillScreen(QWidget):
    def __init__(self, bill_data):
        super().__init__()
        self.setWindowTitle("Your SmartTaxi Bill 🧾")
        self.resize(500, 750)
        self.setMinimumSize(400, 600)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        main_widget = QWidget()
        scroll_area.setWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

        heading = QLabel("SmartTaxi Bill")
        heading.setFont(QFont("Arial", 18, QFont.Bold))
        heading.setStyleSheet("color: #2c3e50; margin-bottom: 10px; padding-left: 10px;")
        heading.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(heading)

        self.add_detail(main_layout, "Name", bill_data['username'])
        self.add_detail(main_layout, "Pickup", bill_data['pickup'])
        self.add_detail(main_layout, "Destination", bill_data['destination'])
        self.add_detail(main_layout, "Distance", f"{bill_data['distance']} km")
        self.add_detail(main_layout, "Amount", f"₹{bill_data['amount']}")

        # save id of the bill in self to update utr in future
        self.bill_id=bill_data["bill_id"]

        main_layout.addSpacing(20)

        self.orderid= int(time.time())

        print(f"DEBUG: bill_id={self.bill_id}, type={type(self.bill_id)}")


        qr_data = f"upi://pay?pa=paytmqr5lwrim@ptys&pn=RAJDIP%20CHANDRAKANT%20PATIL&am={bill_data['amount']}&tr={self.orderid}&tn=taxi%20bill"
        image_path = generate_qr_code(qr_data)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignCenter)
            scaled_pixmap = pixmap.scaled(QSize(300, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            main_layout.addWidget(image_label)
        else:
            print(f"❌ Image not found at: {image_path}")

        main_layout.addSpacing(20)

        # Loader label
        self.loader_label = QLabel("Waiting for confirmation... 0s")
        self.loader_label.setAlignment(Qt.AlignCenter)
        self.loader_label.setStyleSheet("font-size: 14px; color: #2980b9;")
        self.loader_label.hide()
        main_layout.addWidget(self.loader_label)

        # OK Button (initially hidden)
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
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:pressed { background-color: #004085; }
        """)
        self.ok_button.clicked.connect(self.close_bill)
        self.ok_button.hide()  # Hide at start
        main_layout.addWidget(self.ok_button, alignment=Qt.AlignCenter)

        main_layout.setContentsMargins(20, 20, 20, 20)

        # Timer setup
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.poll_payment_status)
        self.elapsed_seconds = 0

        # Start polling
        self.start_polling()

    def add_detail(self, layout, label_text, value):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("color: #34495e; padding-top: 10px; padding-bottom: 5px;")
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)

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
        input_field.setReadOnly(True)
        input_field.setFixedHeight(40)
        layout.addWidget(input_field)
        layout.addSpacing(10)

    def start_polling(self):
        self.loader_label.show()
        self.poll_timer.start(2000)  # every second

    def poll_payment_status(self):
        self.elapsed_seconds += 1
        self.loader_label.setText(f"Waiting for confirmation... {self.elapsed_seconds}s")

        try:
            # 🔁 Replace this with your real API URL
            response = requests.get(f"https://script.google.com/macros/s/AKfycbz6qaJBinOiay49d8yedaK4i_aR2z9ceNZMagJbFbrtBRhoT6uIaYVR7Nrxas74Sl4/exec?order_id={self.orderid}")
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    self.poll_timer.stop()
                    self.loader_label.setText("Payment confirmed ✅")
                     # ✅ Store the UTR number from response
                    self.utr_number = data.get("utr", "N/A")
                    db_handler.update_bill(self.utr_number,self.bill_id)
                    QTimer.singleShot(1000, self.simulate_ok_click)
        except Exception as e:
            print(f"❌ API Polling Error: {e}")

    

    def simulate_ok_click(self):
        self.ok_button.show()
        self.ok_button.click()

    def close_bill(self):
        self.close()
        self.ride_screen = RideScreen(utr_number=self.utr_number)  # dynamic UTR here
        self.ride_screen.show()
