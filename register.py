import cv2
import os

name = input("Enter student name: ").strip()

if not name:
    print("Name cannot be empty.")
    exit()

student_folder = os.path.join("dataset", name)

os.makedirs(student_folder, exist_ok=True)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0

print("\nCamera started.")
print("Look at the camera.")
print("Press Q to stop.\n")

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read from webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        count += 1

        face = frame[y:y + h, x:x + w]

        image_path = os.path.join(
            student_folder,
            f"{count}.jpg"
        )

        cv2.imwrite(image_path, face)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Images: {count}/20",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("Student Registration", frame)

    if cv2.waitKey(100) & 0xFF == ord("q"):
        break

    if count >= 20:
        break

camera.release()
cv2.destroyAllWindows()

print(f"\nRegistration completed for {name}.")
print(f"Saved {count} face images in: {student_folder}")