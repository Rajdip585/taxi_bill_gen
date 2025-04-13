# from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
# from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve
# from modules.billing import BillingHandler
# from modules.maps_api_handler import MapsAPIHandler
# from ui.ride_screen import RideScreen

# class PickupDestinationScreen(QWidget):
#     def __init__(self, username):
#         super().__init__()
#         self.username = username
#         self.setWindowTitle("Enter Trip Details")
#         self.setFixedSize(400, 300)
#         self.maps_handler = MapsAPIHandler()
#         self.init_ui()
#         self.animate_form()
        

#     def init_ui(self):
#         self.label = QLabel(f"Welcome, {self.username}! 🚕", self)
#         self.pickup_input = QLineEdit(self)
#         self.pickup_input.setPlaceholderText("Enter pickup location")

#         self.dest_input = QLineEdit(self)
#         self.dest_input.setPlaceholderText("Enter destination")

#         self.submit_btn = QPushButton("Generate Bill", self)
#         self.submit_btn.clicked.connect(self.generate_bill)

#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.pickup_input)
#         layout.addWidget(self.dest_input)
#         layout.addWidget(self.submit_btn)
#         self.setLayout(layout)
            
#     def animate_form(self):
#         for i, widget in enumerate([self.label, self.pickup_input, self.dest_input, self.submit_btn]):
#             widget.setGeometry(50, 60 + i * 50, 300, 40)  # Set proper geometry first

#             anim = QPropertyAnimation(widget, b"geometry", self)
#             anim.setDuration(700)
#             anim.setStartValue(QRect(50, -50, 300, 40))  # Enter from top
#             anim.setEndValue(QRect(50, 60 + i * 50, 300, 40))  # Land smoothly
#             anim.setEasingCurve(QEasingCurve.OutBounce)
#             anim.start()
            
#             setattr(widget, "_anim", anim)  # Prevent garbage collection


#     def generate_bill(self):
#         pickup = self.pickup_input.text()
#         destination = self.dest_input.text()

#         if not pickup or not destination:
#             QMessageBox.warning(self, "Oops!", "Please enter both pickup and destination.")
#             return

#         try:
#             # 🗺️ Get distance using Maps API
#             distance = self.maps_handler.get_distance_km(pickup, destination)

#             # 💰 Generate bill based on distance
#             billing = BillingHandler()
#             amount = billing.calculate_bill(distance)

#             # 💾 Save to DB
#             billing.generate_and_store_bill(self.username, pickup, destination)

#             # 🎉 Success Message
#             QMessageBox.information(
#                 self,
#                 "Trip Complete 🚗",
#                 f"Distance: {distance:.2f} km\nAmount: ₹{amount:.2f}\nBill saved successfully!"
#             )
#             # 🧼 Close both screens
#             self.close()

#             # 🌟 Show Enjoy Your Ride screen
#             self.ride_screen = RideScreen()
#             self.ride_screen.show()


#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Something went wrong:\n{str(e)}")


from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, QTimer, Qt
from modules.billing import BillingHandler
from modules.maps_api_handler import MapsAPIHandler
from ui.ride_screen import RideScreen
from ui.bill_screen import BillScreen

class PickupDestinationScreen(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Enter Trip Details")
        self.setFixedSize(400, 300)

        self.maps_handler = MapsAPIHandler()

        self.init_ui()
        
        # ✨ Trigger animation *after* the layout is applied
        QTimer.singleShot(100, self.animate_form)

    def init_ui(self):
        # 🌞 Light theme
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', sans-serif;
                color: #212529;
            }

            QLabel {
                font-size: 30px;
                font-weight: 600;
                margin-bottom: 6px;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                background-color: #fff;
                color: #495057;
            }

            QLineEdit:focus {
                border-color: #80bdff;
                outline: none;
                background-color: #fff;
            }

            QPushButton {
                background-color: #0d6efd;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)


        self.label = QLabel(f"Welcome, {self.username}! 🚕", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.pickup_input = QLineEdit(self)
        self.pickup_input.setPlaceholderText("Enter pickup location")

        self.dest_input = QLineEdit(self)
        self.dest_input.setPlaceholderText("Enter destination")

        self.submit_btn = QPushButton("Generate Bill", self)
        self.submit_btn.clicked.connect(self.generate_bill)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.pickup_input)
        layout.addWidget(self.dest_input)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def animate_form(self):
        for widget in [self.label, self.pickup_input, self.dest_input, self.submit_btn]:
            anim = QPropertyAnimation(widget, b"geometry")
            anim.setDuration(600)
            anim.setStartValue(QRect(widget.x() - 400, widget.y(), widget.width(), widget.height()))
            anim.setEndValue(QRect(widget.x(), widget.y(), widget.width(), widget.height()))
            anim.setEasingCurve(QEasingCurve.OutBounce)
            anim.start()
            setattr(widget, "_anim", anim)

    def generate_bill(self):
        pickup = self.pickup_input.text()
        destination = self.dest_input.text()

        if not pickup or not destination:
            QMessageBox.warning(self, "Oops!", "Please enter both pickup and destination.")
            return

        try:
            distance = self.maps_handler.get_distance_km(pickup, destination)
            billing = BillingHandler()
            amount = billing.calculate_bill(distance)
            billing.generate_and_store_bill(self.username, pickup, destination)

            # QMessageBox.information(
            #     self,
            #     "Trip Complete 🚗",
            #     f"Distance: {distance:.2f} km\nAmount: ₹{amount:.2f}\nBill saved successfully!"
            # )
            
            bill_data = {'username': self.username, 'pickup': pickup, 'destination': destination, 'distance': distance, 'amount': amount}
            self.bill_screen = BillScreen(bill_data)
            self.bill_screen.show()

            self.close()  # Optional: close after billing
            
            # 🌟 Show Enjoy Your Ride screen
            # self.ride_screen = RideScreen()
            # self.ride_screen.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong:\n{str(e)}")
