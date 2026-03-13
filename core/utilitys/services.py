import json
from pathlib import Path
import sys
import yt_dlp
import os
import django
import whisper
from google import genai
from .base_prompt import base_prompt


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from django.conf import settings

def video_to_quiz(url, request =None):
    clean_url = transform_yt_url(url, request)
    sound_path = download_mp3(clean_url, request)["relative_path"]
    transcript = transcribe_audio(sound_path)
    quiz_as_string = convert_transcript_to_quiz(transcript, request)
    quiz_as_JSON = _convert_quiz_to_JSON_dict(quiz_as_string, request)
    _delete_media_file(sound_path)
    return quiz_as_JSON

def transform_yt_url(url, request):
    base_url = "https://www.youtube.com/watch?v="
    
    if "https://youtu.be/" in url:
        video_id = url[17:28]
        return base_url + video_id
    
    return url

def download_mp3(url: str, request) -> dict:
    """
    Lädt Audio per yt-dlp herunter, konvertiert zu mp3
    und speichert die Datei unter MEDIA_ROOT/downloads/mp3/.

    Rückgabe:
        {
            "title": "...",
            "filename": "...mp3",
            "relative_path": "downloads/mp3/...mp3",
            "absolute_path": "/.../media/downloads/mp3/...mp3"
        }
    """
    # from django.conf import settings

    target_dir = Path(settings.MEDIA_ROOT) / "downloads" / "mp3"
    target_dir.mkdir(parents=True, exist_ok=True)

    # yt-dlp ersetzt %(ext)s nach der Konvertierung passend
    outtmpl = str(target_dir / "%(title).200B-%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # Nach Postprocessing ist requested_downloads oft am hilfreichsten
        requested = info.get("requested_downloads") or []
        if requested and requested[0].get("filepath"):
            final_path = Path(requested[0]["filepath"])
        else:
            # Fallback
            final_path = next(target_dir.glob(f"*{info.get('id', '')}*.mp3"), None)

        if not final_path or not final_path.exists():
            raise FileNotFoundError("MP3-Datei wurde nicht gefunden.")

        relative_path = final_path.relative_to(settings.MEDIA_ROOT)

        return {
            "title": info.get("title"),
            "filename": final_path.name,
            "relative_path": str(relative_path).replace("\\", "/"),
            "absolute_path": str(final_path),
        }
    
def transcribe_audio(relative_path: str, model_name: str = "turbo") -> dict:
    """
    Nimmt einen relativen Pfad unter MEDIA_ROOT, transkribiert die Audiodatei
    und gibt Whisper-Ergebnisse zurück.
    """
    absolute_path = Path(settings.MEDIA_ROOT) / relative_path

    if not absolute_path.exists():
        raise FileNotFoundError(f"Audio-Datei nicht gefunden: {absolute_path}")

    model = whisper.load_model(model_name)
    result = model.transcribe(str(absolute_path))

    return {
        "text": result.get("text", "").strip(),
        "language": result.get("language"),
        "segments": result.get("segments", []),
        "absolute_path": str(absolute_path),
    }

def convert_transcript_to_quiz(transcript, request):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=base_prompt + transcript['text'],
    )
    print(response.text)
    return response.text

def _convert_quiz_to_JSON_dict(quiz, response):
    return json.loads(quiz)


def _delete_media_file(relative_path: str) -> bool:
    """
    Löscht eine Datei unter MEDIA_ROOT anhand ihres relativen Pfades.

    Beispiel:
        relative_path = "downloads/mp3/video.mp3"
    """
    file_path = Path(settings.MEDIA_ROOT) / relative_path

    if file_path.exists():
        file_path.unlink()
        return True

    return False





