
from flask import Flask, render_template, Response, jsonify
import os
import pandas as pd
from datetime import datetime

from main import generate_frames, start_camera, stop_camera


app = Flask(__name__)

ATTENDANCE_FILE = "attendance.csv"
DATASET_PATH = "dataset"


# ==========================================
# GET REGISTERED STUDENTS
# ==========================================

def get_students():

    if os.path.exists(DATASET_PATH):

        students = [
            folder
            for folder in os.listdir(DATASET_PATH)
            if os.path.isdir(
                os.path.join(DATASET_PATH, folder)
            )
        ]

    else:

        students = []

    return sorted(students)


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/")
def home():

    students = get_students()

    total_students = len(students)


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


    today = datetime.now().strftime("%Y-%m-%d")


    today_attendance = df[
        df["Date"].astype(str) == today
    ]


    present_today = len(today_attendance)


    if total_students > 0:

        attendance_rate = round(
            (present_today / total_students) * 100
        )

    else:

        attendance_rate = 0


    return render_template(

        "index.html",

        total_students=total_students,

        present_today=present_today,

        attendance_rate=attendance_rate

    )


# ==========================================
# START CAMERA
# ==========================================

@app.route("/start-camera")
def start_camera_route():

    success = start_camera()

    if success:

        return jsonify({
            "status": "started"
        })

    return jsonify({
        "status": "error"
    }), 500


# ==========================================
# STOP CAMERA
# ==========================================

@app.route("/stop-camera")
def stop_camera_route():

    stop_camera()

    return jsonify({
        "status": "stopped"
    })


# ==========================================
# LIVE CAMERA FEED
# ==========================================

@app.route("/video_feed")
def video_feed():

    return Response(

        generate_frames(),

        mimetype=
        "multipart/x-mixed-replace; boundary=frame"

    )


# ==========================================
# ATTENDANCE RECORDS
# ==========================================

@app.route("/attendance")
def attendance():

    if os.path.exists(ATTENDANCE_FILE):

        df = pd.read_csv(ATTENDANCE_FILE)

        records = df.to_dict("records")

    else:

        records = []


    return render_template(

        "attendance.html",

        attendance=records

    )


# ==========================================
# STUDENTS
# ==========================================

@app.route("/students")
def students():

    student_list = get_students()


    return render_template(

        "students.html",

        students=student_list

    )


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)

