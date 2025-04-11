from face_recognition_handler import FaceRecognizer

recognizer = FaceRecognizer()
name = recognizer.recognize_face()
print(f"Hello, {name}!" if name != "Unknown" else "Face not recognized.")
