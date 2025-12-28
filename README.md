# Tawasol (تواصل) - Arabic Sign Language Translator

[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


![Project Demo](https://github.com/user-attachments/assets/716a36e7-d834-447d-b86c-b40c631a0735)

Tawasol is a real-time communication tool designed to bridge the gap between the hearing-impaired community and the general public by translating Arabic sign language into text.

---

### ✨ Key Features

| Feature                   | Description                                                                                               | Screenshot                                                                                                                                  |
| ------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Real-Time Translation** | Utilizes a webcam to capture hand gestures and translates them into Arabic text instantly. | ![Real-Time Translation](https://github.com/user-attachments/assets/3a974340-f36d-4ba8-ba83-2398201aba8c) ![Real-Time Translation Demo](https://github.com/user-attachments/assets/346b167f-d0e1-4434-a596-327f62f17d83) |
| **User & Patient Management** | A comprehensive web interface for administrators to manage users (employees) and patients.              | ![User & Patient Management](https://github.com/user-attachments/assets/53d9740f-1404-4377-ab49-971f081db76a) |
| **Admin Dashboard**       | A dedicated dashboard for administrators to manage the application's users and data.                      | ![Admin Dashboard](https://github.com/user-attachments/assets/2ff74c28-93fe-4c0a-b84a-f11097a551ef)                                       |
| **Conversation Logging**  | Securely logs translated conversations for each patient, providing a history for review.                  |                                                                                                                        |
| **PDF Export**            | Allows for the exporting of patient conversation logs into a PDF format for official records. |                                                                                                                          |

---

### 🚀 My Contribution

In this project, I spearheaded the development of the core backend infrastructure and the integration of the machine learning components. My key contributions include:

-   **Backend Development:** Designing and implementing the Flask application's backend logic, API endpoints, and database interactions.
-   **Dataset Creation:** Personally collecting and annotating the Arabic sign language gestures to build a robust dataset tailored for this application.
-   **Model Development & Training:** Developing, training, and fine-tuning the machine learning models for real-time gesture recognition.

This comprehensive involvement ensures the project's robust functionality from data to deployment-ready backend.

---

### 🛠️ Technology Stack

-   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Migrate
-   **Machine Learning:** TensorFlow/Keras, OpenCV, CVZone, MediaPipe
-   **Database:** SQLite
-   **Frontend:** HTML, CSS, JavaScript
-   **Deployment:** Docker (see *Project Improvements*)

---

### 📋 Getting Started

Follow these steps to get the project running on your local machine.

#### Prerequisites

-   Git
-   Conda (Miniconda or Anaconda)
-   A webcam

#### Project Improvements (Recommended First Steps)

*Senior Note: Before others can use your project, we need to fix the dependency list. Your `requirements.txt` is incomplete. Also, the Python version in your `Dockerfile` (3.11) doesn't match the project's dependencies (`mediapipe` wheel is for Python 3.9). Here's how to fix it:*

1.  **Activate your environment:** `conda activate ./.conda`
2.  **Generate a complete `requirements.txt`:**
    ```bash
    pip freeze > requirements.txt
    ```
3.  **Commit the change:**
    ```bash
    git add requirements.txt
    git commit -m "Update requirements.txt with all dependencies"
    ```
4.  **Update your `Dockerfile`:** Change the first line from `FROM python:3.11-slim` to `FROM python:3.9-slim` to match your project's environment. Then commit that change.

#### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:Abdullrahman-Jameel/Arabic_Sign_Lang.git
    cd Arabic_Sign_Lang
    ```

2.  **Download the Model:**
    The gesture recognition model (`keras_model_12.h5`) is not included in this repository due to its size. Please download it and place it inside the `models/` directory.
    
    *Senior Note: For a truly professional setup, you should upload this model file to a service like Google Drive, Dropbox, or learn to use [Git LFS (Large File Storage)](https://git-lfs.github.com/) and update this link.*
    
    [**Download Model Here**](<YOUR_MODEL_DOWNLOAD_LINK_HERE>)

3.  **Create and Activate the Conda Environment:**
    This command creates a local Conda environment using the correct Python version (3.9) and activates it.
    ```bash
    conda create --prefix ./.conda python=3.9
    conda activate ./.conda
    ```

4.  **Install Dependencies:**
    (If you completed the "Project Improvements" step, this will now install everything correctly).
    ```bash
    pip install -r requirements.txt
    ```

5.  **Initialize the Database:**
    Run this script once to create the database file and the default admin user.
    ```bash
    python init_db.py
    ```
    -   **Admin Email:** `admin@tawasol.com`
    -   **Admin Password:** `password`

6.  **Run the Application:**
    ```bash
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

### 📄 License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
*(Senior Note: I've assumed an MIT license. You should create a file named `LICENSE.md`, paste the MIT license text into it, and commit it.)*
