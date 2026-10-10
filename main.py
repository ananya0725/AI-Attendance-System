
from deepface import DeepFace
import cv2
import os
import pandas as pd
from datetime import datetime
import threading


DATASET_PATH = "dataset"
ATTENDANCE_FILE = "attendance.csv"


# ==========================================
# CAMERA CONTROL
# ==========================================

camera = None
camera_running = False
camera_lock = threading.Lock()


# ==========================================
# ATTENDANCE
# ==========================================

def mark_attendance(name):

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    if os.path.exists(ATTENDANCE_FILE):

        df = pd.read_csv(ATTENDANCE_FILE)

    else:

        df = pd.DataFrame(
            columns=[
                "Name",
                "Date",
                "Time",
                "Status"
            ]
        )

    already_marked = (
        (df["Name"] == name) &
        (df["Date"] == today)
    ).any()

    if not already_marked:

        new_record = pd.DataFrame([{

            "Name": name,
            "Date": today,
            "Time": current_time,
            "Status": "Present"

        }])

        df = pd.concat(
            [df, new_record],
            ignore_index=True
        )

        df.to_csv(
            ATTENDANCE_FILE,
            index=False
        )

        print(f"Attendance marked: {name}")

        return True

    return False


# ==========================================
# START CAMERA
# ==========================================

def start_camera():

    global camera
    global camera_running

    with camera_lock:

        if camera_running:
            return True

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():

            camera = None
            camera_running = False

            print("Error: Could not open webcam.")

            return False

        camera_running = True

        print("Camera started.")

        return True


# ==========================================
# STOP CAMERA
# ==========================================

def stop_camera():

    global camera
    global camera_running

    with camera_lock:

        camera_running = False

        if camera is not None:

            camera.release()

            camera = None

        print("Camera stopped.")


# ==========================================
# CAMERA STREAM
# ==========================================

def generate_frames():

    global camera
    global camera_running

    if not start_camera():

        return


    while camera_running:

        with camera_lock:

            if camera is None:

                break

            success, frame = camera.read()


        if not success:

            break


        recognized_name = None


        # ==================================
        # FACE RECOGNITION
        # ==================================

        try:

            result = DeepFace.find(

                img_path=frame,

                db_path=DATASET_PATH,

                model_name="Facenet512",

                detector_backend="opencv",

                enforce_detection=False,

                silent=True

            )


            if len(result) > 0 and not result[0].empty:

                identity = result[0].iloc[0]["identity"]

                recognized_name = os.path.basename(
                    os.path.dirname(identity)
                )

                mark_attendance(recognized_name)


        except Exception:

            pass


        # ==================================
        # DISPLAY STATUS
        # ==================================

        if recognized_name:

            cv2.putText(

                frame,

                f"Recognized: {recognized_name}",

                (20, 40),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.9,

                (0, 255, 0),

                2

            )

        else:

            cv2.putText(

                frame,

                "Scanning face...",

                (20, 40),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.9,

                (255, 255, 255),

                2

            )


        # ==================================
        # ENCODE FRAME
        # ==================================

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not ret:

            continue


        frame_bytes = buffer.tobytes()


        yield (

            b"--frame\r\n"

            b"Content-Type: image/jpeg\r\n\r\n"

            + frame_bytes +

            b"\r\n"

        )


    # ======================================
    # RELEASE CAMERA
    # ======================================

    stop_camera()

