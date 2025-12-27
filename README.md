# Tawasol (تواصل) - Arabic Sign Language Translator

Tawasol is a real-time communication tool designed to bridge the gap between the hearing-impaired community and the general public by translating Arabic sign language into text. This project was built from the ground up, including personal data collection and model training, to ensure a tailored and effective solution.

## Key Features

- **Real-Time Translation:** Utilizes a webcam to capture hand gestures and translates them into Arabic text instantly.
- **User & Patient Management:** A comprehensive Flask-based web interface for administrators to manage users (employees) and patients.
- **Conversation Logging:** Securely logs translated conversations for each patient, providing a history for review.
- **PDF Export:** Allows for the exporting of patient conversation logs into a PDF format for record-keeping.
- **Admin Dashboard:** A dedicated dashboard for administrators to manage the application's users and data.

## My Contribution

As the sole developer, I was responsible for all aspects of this project. A significant part of this work involved creating the dataset from scratch. I personally recorded and annotated the sign language gestures used to train the machine learning model, ensuring high-quality and relevant data for the specific use case of this application. The gesture recognition model was also trained and fine-tuned by me.

## Technology Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Machine Learning:** TensorFlow/Keras, OpenCV, CVZone, MediaPipe
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Deployment:** Docker

## Project Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

- **Git:** You need Git installed to clone the repository.
- **Conda:** The project uses a Conda environment. You can install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you don't have it.
- **Webcam:** Required for the real-time translation feature.

### 2. Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:Abdullrahman-Jameel/Arabic_Sign_Lang.git
    cd Arabic_Sign_Lang
    ```

2.  **Download the Model:**
    The gesture recognition model (`keras_model_12.h5`) is not included in this repository due to its size. Please download it from [this link](<YOUR_MODEL_DOWNLOAD_LINK_HERE>) and place it inside the `models/` directory.
    *(Senior Note: We should host this on a service like Google Drive, Dropbox, or use Git LFS and replace the link above.)*

3.  **Create and Activate the Conda Environment:**
    This project runs on Python 3.9. The following commands will create a local Conda environment in the `.conda/` directory and activate it.
    ```bash
    conda create --prefix ./.conda python=3.9
    conda activate ./.conda
    ```

4.  **Install Dependencies:**
    The `requirements.txt` file is currently incomplete. First, install the listed packages, then manually install `cvzone` and `mediapipe`.
    *(Senior Note: A good next step would be to create a complete `requirements.txt` by running `pip freeze > requirements.txt` in your activated environment and committing the updated file.)*
    ```bash
    pip install -r requirements.txt
    pip install cvzone==1.5.6 mediapipe==0.8.9.1
    ```

5.  **Initialize the Database:**
    Run this script once to create the database file and the default admin user.
    ```bash
    python init_db.py
    ```
    - **Admin Email:** `admin@tawasol.com`
    - **Admin Password:** `password`

6.  **Run the Application:**
    ```bash
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

## How to Use

- **Admin Login:** Use the credentials above to log into the admin dashboard and manage users.
- **Translator Interface:** Access the `/translator` page to start the real-time sign language translation.
