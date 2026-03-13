# Quizly

Quizly is a backend API that automatically generates quizzes from YouTube videos.
The system downloads the audio from a video, transcribes it, and uses AI to generate quiz questions.

The result is a structured quiz with multiple questions and answer options that can be consumed by any frontend application.

## Features

- Generate quizzes automatically from YouTube videos
- Download and convert video audio to MP3
- Transcribe audio using speech-to-text
- Generate quiz questions using AI
- Store quizzes and questions in a database
- REST API for creating, retrieving, updating, and deleting quizzes
- Authentication and permissions for user-owned quizzes

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework

### AI / Processing
- yt-dlp (YouTube audio download)
- Whisper (speech-to-text transcription)
- Google Gemini API (quiz generation)

### Database
- SQLite (default, development)

## API Endpoints
Base path:

`/api/quizzes/`

#### Create Quiz

Generate a new quiz from a YouTube video.

`POST /api/quizzes/`

Request:

{
  "url": "https://youtu.be/example"
}

Response:

{
  "id": 1,
  "title": "Quiz Title",
  "description": "Quiz Description",
  "created_at": "...",
  "updated_at": "...",
  "video_url": "...",
  "questions": [
    {
      "id": 1,
      "question_title": "Question 1",
      "question_options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option A"
    }
  ]
}
List Quizzes
GET /api/quizzes/

Returns all quizzes owned by the authenticated user.

Retrieve Quiz
GET /api/quizzes/{id}/

Returns a single quiz with all questions.

Update Quiz (Partial)
PATCH /api/quizzes/{id}/

Example:

{
  "title": "Updated Quiz Title"
}
Delete Quiz
DELETE /api/quizzes/{id}/

Deleting a quiz will also delete all associated questions.

Permissions
Action	Requirement
Create	Authenticated user
List	Authenticated user
Retrieve	Owner only
Update	Owner only
Delete	Owner only
Installation

Clone the repository:

git clone https://github.com/SchrimpsMitReis/Quizly.git
cd Quizly

Create a virtual environment:

python -m venv env

Activate it:

Windows

env\Scripts\activate

Linux / Mac

source env/bin/activate

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file and configure your API keys.

Example:

GEMINI_API_KEY=your_api_key_here
Run Migrations
python manage.py migrate
Start the Server
python manage.py runserver

API will be available at:

http://127.0.0.1:8000/api/
Project Structure
Quizly
│
├── core
│   ├── settings.py
│   ├── urls.py
│
├── quiz_app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│
├── utilitys
│   ├── services.py
│   ├── audio_processing.py
│
└── manage.py
Future Improvements

Frontend interface

Background task processing (Celery / Redis)

Quiz difficulty settings

Multiple language support

Pagination and filtering

License

MIT License

If you want, I can also help you create:

a much more impressive README (GitHub-style with badges, API diagrams, and architecture)

an architecture section explaining the AI pipeline

or a cool project banner for the repo.

das klingt klasse, mach das!

Super — dann bauen wir dir eine richtig gute GitHub-README, wie man sie bei ernsthaften Open-Source-Projekten sieht.
Mit:

Badges

Architekturdiagramm

AI-Pipeline

API-Übersicht

Installation

Beispielresponse

sauberem Layout

Du kannst das 1:1 als README.md benutzen.

🧠 Quizly
Generate quizzes automatically from YouTube videos








Quizly is an AI-powered backend API that automatically generates quizzes from YouTube videos.

The system extracts audio from a video, transcribes it using speech-to-text, and uses AI to generate structured quiz questions with multiple answers.

The result is a ready-to-use quiz that can be consumed by any frontend application.

🚀 Features

🎥 Generate quizzes directly from YouTube videos

🎧 Automatic audio extraction

🗣 Speech-to-text transcription using Whisper

🤖 AI-generated quiz questions

📚 Store quizzes and questions in a database

🔐 Authentication & ownership permissions

🌐 REST API built with Django REST Framework

🧠 How It Works

Quizly processes videos in several steps.

YouTube Video
      │
      ▼
Download Audio (yt-dlp)
      │
      ▼
Convert to MP3
      │
      ▼
Speech-to-Text (Whisper)
      │
      ▼
AI Question Generation (Gemini)
      │
      ▼
Quiz JSON Structure
      │
      ▼
Saved to Database

Result:

Quiz
 ├── Question
 │     ├── Option A
 │     ├── Option B
 │     ├── Option C
 │     └── Option D
 └── Question
🏗 Architecture
Frontend (optional)
       │
       ▼
REST API (Django REST Framework)
       │
       ├── Authentication
       ├── Permissions
       │
       ▼
Quiz Generation Service
       │
       ├── yt-dlp
       ├── Whisper
       └── Gemini AI
       │
       ▼
Database
       │
       ├── Quiz
       └── Question
🧰 Tech Stack
Backend

Python

Django

Django REST Framework

AI / Processing

yt-dlp

Whisper

Google Gemini API

Database

SQLite (development)

📡 API Overview

Base endpoint

/api/quizzes/
Create Quiz

Generate a quiz from a YouTube video.

POST /api/quizzes/

Request

{
  "url": "https://youtu.be/example"
}

Response

{
  "id": 1,
  "title": "Quiz Title",
  "description": "Quiz Description",
  "created_at": "2023-07-29T12:34:56.789Z",
  "updated_at": "2023-07-29T12:34:56.789Z",
  "video_url": "https://www.youtube.com/watch?v=example",
  "questions": [
    {
      "id": 1,
      "question_title": "Question 1",
      "question_options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option A"
    }
  ]
}
List Quizzes
GET /api/quizzes/

Returns all quizzes belonging to the authenticated user.

Retrieve Quiz
GET /api/quizzes/{id}/

Returns one quiz with all questions.

Update Quiz
PATCH /api/quizzes/{id}/

Example

{
  "title": "Updated Quiz Title"
}
Delete Quiz
DELETE /api/quizzes/{id}/

Deleting a quiz also deletes all related questions.

🔐 Permissions
Action	Requirement
Create	Authenticated user
List	Authenticated user
Retrieve	Owner only
Update	Owner only
Delete	Owner only
⚙️ Installation

Clone the repository

git clone https://github.com/SchrimpsMitReis/Quizly.git
cd Quizly

Create virtual environment

python -m venv env

Activate environment

Windows

env\Scripts\activate

Mac / Linux

source env/bin/activate

Install dependencies

pip install -r requirements.txt
🔑 Environment Variables

Create a .env file.

Example

GEMINI_API_KEY=your_api_key_here
🗄 Run Migrations
python manage.py migrate
▶ Run Server
python manage.py runserver

API available at

http://127.0.0.1:8000/api/
📁 Project Structure
Quizly
│
├── core
│   ├── settings.py
│   ├── urls.py
│
├── quiz_app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│
├── utilitys
│   ├── services.py
│   ├── audio_processing.py
│
└── manage.py
🧪 Testing

API endpoints can be tested using:

Postman

curl

Django test client

Example

POST /api/quizzes/

with JSON body:

{
"url": "https://youtu.be/example"
}
🛣 Future Improvements

Async quiz generation (Celery)

Frontend interface

Quiz difficulty settings

Multi-language transcription

Rate limiting

Pagination and filtering

📜 License

MIT License

👨‍💻 Author

Roman Schröder

GitHub

https://github.com/SchrimpsMitReis

Optional (sehr empfehlenswert)

Wenn du willst, kann ich dir noch zusätzlich bauen:

ein Architekturdiagramm als Bild für GitHub

ein cooles Repo Banner

GitHub Contribution Graph für dein Repo

API Documentation Section (Swagger / OpenAPI)
