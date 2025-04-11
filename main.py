from modules import db_handler
import sys
from PyQt5.QtWidgets import QApplication, QLabel
from ui.face_scan_screen import FaceRecognizer, FaceScanScreen

db_handler.create_tables()
db_handler.log_user("Gunjan")

app = QApplication(sys.argv)
window = FaceScanScreen()
window.show()
sys.exit(app.exec_())
