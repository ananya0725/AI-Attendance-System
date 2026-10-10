# AI Attendance System Using Face Recognition

An AI-powered attendance management system that uses face recognition to identify registered students and automatically record their attendance.

## Overview

Manual attendance can be time-consuming and prone to errors. This project uses computer vision and deep learning-based face recognition to simplify attendance tracking.

## Features

* **Student Registration:** Register students by capturing face images.
* **Face Detection:** Detect faces using OpenCV.
* **Face Recognition:** Identify registered students using DeepFace.
* **Automatic Attendance:** Record the student's name, date, time, and status.
* **Duplicate Prevention:** Avoid marking the same student present more than once per day.
* **Attendance Dashboard:** View attendance records through a web interface.
* **Student Directory:** View registered student profiles.

## Technologies Used

* Python
* OpenCV
* DeepFace
* TensorFlow
* Pandas
* Flask
* HTML and CSS
* CSV for attendance storage

## Project Structure

```text
AI Attendance/
├── app.py
├── main.py
├── register.py
├── attendance.csv
├── dataset/
├── templates/
│   ├── index.html
│   ├── attendance.html
│   └── students.html
├── static/
│   └── style.css
├── .gitignore
└── README.md
```

## Download and Installation

### Download the Project

Download the complete project as a ZIP file.


### Installation

1. Extract the downloaded ZIP file.

2. Open the extracted `AI-Attendance-System` folder in VS Code.

3. Open the terminal in that folder.

4. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

5. Install the required libraries:

   ```bash
   pip install opencv-python==4.10.0.84 deepface pandas flask tf-keras
   ```

6. Register students by running:

   ```bash
   python register.py
   ```

7. Start the application:

   ```bash
   python app.py
   ```

8. Open http://127.0.0.1:5000 in your browser.


## How It Works

1. Capture and store images of registered students.
2. Start the webcam from the dashboard.
3. Detect and compare faces against the registered dataset.
4. Identify a matching student.
5. Record attendance with the current date and time.
6. Display attendance records on the dashboard.

## Important Notes

* This project is intended for educational and demonstration purposes.
* A webcam is required for student registration and face recognition.
* Face images are not included in this repository. Register students locally before using the system.
* Keep biometric data and attendance records private.
* Recognition accuracy may vary with lighting, camera quality, and face positioning.

## Future Enhancements

* Database integration
* Attendance reports and CSV export
* Search and date-based filtering
* Improved recognition performance
* Authentication for administrators

## License

This project is available for educational and learning purposes.
