from modules import db_handler
import face_recognition
import cv2
import os
from PyQt5.QtWidgets import QInputDialog


class FaceRecognizer:
    def __init__(self, known_faces_dir="images/known_faces"):
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                img_path = os.path.join(self.known_faces_dir, filename)
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.known_face_encodings.append(encodings[0])
                    name = os.path.splitext(filename)[0]
                    self.known_face_names.append(name)
                    print(f"[INFO] Loaded face for: {name}")
                else:
                    print(f"[WARNING] No face found in {filename}")

    def recognize_face(self):
        # 👀 Try this to debug
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Camera index {i} is working 🎥")
                break
            cap.release()
        else:
            print("No camera found 😭")
            return None
        # cap = cv2.VideoCapture(0)
        print("[INFO] Scanning for face...")

        while True:
            ret, frame = cap.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                if face_distances.size > 0:
                    best_match_index = face_distances.argmin()
                    confidence = face_distances[best_match_index]
                    
                    if matches[best_match_index] and confidence < 0.5:
                        name = self.known_face_names[best_match_index]
                    else:
                        name = "Unknown"
                        
                        # ✨ NEW FACE HANDLING MAGIC STARTS HERE ✨

                        # Show webcam preview for the user
                        cv2.imshow("New Face Detected", frame)
                        cv2.waitKey(1000)

                        # Ask for their name (PyQt or input())
                        from PyQt5.QtWidgets import QInputDialog
                        user_name, ok = QInputDialog.getText(None, "New User", "Enter your name:")

                        if ok and user_name:
                            # Save full frame (or crop to face later if you want)
                            filename = f"{user_name}.jpg"
                            save_path = os.path.join(self.known_faces_dir, filename)
                            cv2.imwrite(save_path, frame)
                            print(f"[INFO] Saved new face as {filename}")

                            # Add to DB
                            db_handler.log_user(user_name)

                            # Encode & add to memory (so no restart needed)
                            new_image = face_recognition.load_image_file(save_path)
                            new_encodings = face_recognition.face_encodings(new_image)
                            if new_encodings:
                                self.known_face_encodings.append(new_encodings[0])
                                self.known_face_names.append(user_name)
                                print(f"[INFO] {user_name} is now known 🎉")

                            name = user_name

                        else:
                            print("[INFO] User canceled name entry. Not saving new face.")
                        
                        # 💾 Log recognized user
                        # db_handler.log_user(name)
                        
                # Show result
                print(f"[RESULT] Detected face: {name}")
                cap.release()
                cv2.destroyAllWindows()
                return name

            # Show webcam preview (optional)
            cv2.imshow('Face Recognition - Press Q to Quit', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return None
