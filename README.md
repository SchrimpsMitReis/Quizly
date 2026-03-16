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
## AI Setup

Quizly uses several AI and media-processing tools to automatically generate quizzes from YouTube videos.
Before running the project, these dependencies must be installed and configured. 

**Whisper, YT-dlp and Gemini already exist on the requirements.txt**

**Just ffmpeg should be installed cause it's no Python Package!**

**In case of Gemini just start with the .env file**
## Whisper (Speech-to-Text)

Quizly uses OpenAI Whisper to transcribe the audio of YouTube videos into text.
The transcription is later used as input for the quiz generation process.

Install Whisper with:
```
pip install openai-whisper
```
Whisper also requires FFmpeg to process audio files.

Install FFmpeg:

#### Windows

Download FFmpeg from:
```
https://ffmpeg.org/download.html
```
After installation, make sure the ffmpeg binary is available in your system PATH.

#### Linux
```
sudo apt install ffmpeg
```
#### Mac
```
brew install ffmpeg
```
## yt-dlp (YouTube Downloader)

Quizly uses yt-dlp to download the audio track from YouTube videos and convert it into MP3 format.

Install it with:
```
pip install yt-dlp
```
The downloader extracts the best available audio stream and converts it into an MP3 file that can be processed by Whisper.

## Google Gemini API (Quiz Generation)

The quiz questions are generated using Google Gemini AI.

Install the client library:
```
pip install google-genai
```
You must also provide an API key.

Create a .env file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```
You can obtain a Gemini API key from:
```
https://ai.google.dev/
```
The Gemini model is used to convert the transcript into structured quiz questions.

## AI Processing Pipeline

The quiz generation process works as follows:
```
YouTube Video
      │
      ▼
Download Audio (yt-dlp)
      │
      ▼
Convert to MP3
      │
      ▼
Transcription (Whisper)
      │
      ▼
Quiz Generation (Gemini)
      │
      ▼
Structured Quiz JSON
      │
      ▼
Stored in Database
```
### Notes

Whisper models are downloaded automatically on first use.

Large videos may take longer to process depending on the selected Whisper model.

The Gemini API requires a valid API key and internet connection.
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

