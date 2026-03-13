___
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

``` /api/quizzes/ ```
___
### Create Quiz

Generate a new quiz from a YouTube video.

``` python POST /api/quizzes/ ```

Request:

``{ "url": "https://youtu.be/example" }``

Response:

````{
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
````
___
### List Quizzes
GET /api/quizzes/

Returns all quizzes owned by the authenticated user.
___
### Retrieve Quiz
``GET /api/quizzes/{id}/``

Returns a single quiz with all questions.

Update Quiz (Partial)

``PATCH /api/quizzes/{id}/``

Example:

```
{
  "title": "Updated Quiz Title"
}
```
___
### Delete Quiz
DELETE /api/quizzes/{id}/

Deleting a quiz will also delete all associated questions.
___
## Permissions
```
| Action |	Requirement |
| Create |	Authenticated user |
| List    |	Authenticated user |
| Retrieve |	Owner only |
| Update |	Owner only |
| Delete |	Owner only |
```
___
## Installation

Clone the repository:

```
git clone https://github.com/SchrimpsMitReis/Quizly.git
cd Quizly
```
Create a virtual environment:

```
python -m venv env
```

Activate it:

Windows
```
env\Scripts\activate
```
Linux / Mac
```
source env/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```
___
### Environment Variables

Create a .env file and configure your API keys.

Example:

GEMINI_API_KEY=your_api_key_here
___
### Run Migrations

python manage.py migrate
___
### Start the Server
python manage.py runserver

API will be available at:

http://127.0.0.1:8000/api/
___
### Project Structure
```
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
```
___
### Future Improvements

- Frontend interface
- Background task processing (Celery / Redis)
- Quiz difficulty settings
- Multiple language support
- Pagination and filtering
___
### License

MIT License

