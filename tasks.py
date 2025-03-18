# tasks.py
from celery_config import celery
import yt_dlp as youtube_dl

@celery.task
def download_video(url):
    try:
        ydl_opts = {
            'nocheckcertificate': True,  # Ignore SSL certificate verification
            'format': 'best',  # Choose the best quality format
            'outtmpl': 'static/downloads/%(title)s.%(ext)s',  # Save videos with their original names and extensions
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  # Download the video
            title = info['title']
            filepath = ydl.prepare_filename(info)  # Get the full path to the downloaded file
            return {'title': title, 'url': url, 'filepath': filepath}
    except Exception as e:
        print("Error:", e)
        return None