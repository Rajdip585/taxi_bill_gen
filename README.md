🚖 SmartTaxi — Face Recognition Billing System

An intelligent and fun taxi billing system that uses face recognition to identify users, calculate trip distance using the OpenRouteService Maps API, and generate bills automatically based on the distance traveled. Built with Python, PyQt5, OpenCV, and a whole lotta love 💛


🔥 Features:

👤 Face Recognition Login – Recognize returning users or auto-register new ones.
📸 Face Model Self-Training – Improves accuracy by saving new images with each successful recognition.
🗺️ Live Distance Calculation – Uses OpenRouteService to get real-world driving distance between pickup and destination.
💸 Auto Bill Generation – Calculates fare instantly (customizable per-km rate).
🖤 Dark Mode UI – Clean, modern, and fun interface with bouncy animations.
🧠 SQLite DB – Stores trip history and user records securely.
🔒 No manual login – Just show your face, and you’re good to go.


⚙️ Tech Stack

Python 3
PyQt5
OpenCV
face_recognition
OpenRouteService API
SQLite
dotenv


🧪 How It Works

Open the app — scan your face.
If you're new, your face gets saved and you're registered.
Enter pickup & destination — the system calculates distance.
You get a bill instantly — and it's saved in the DB.
App closes with a smile and a screen saying "Enjoy your ride" 😊


🚀 Future Plans

 Add light/dark mode toggle ☀️🌑
 Full trip history dashboard
 Export bills as PDFs
 Integrate GPS tracking
