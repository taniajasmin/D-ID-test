import base64
import requests
import time
import os
import sys

DID_KEY = "YmFua3Byb2NvaW5AZ21haWwuY29t:T5WmlTQYwBpQ1NlTBy17k"
AUDIO_FILE = "silence5s.mp3"
OUTPUT_FILE = "amy_silent.mp4"
PRESENTER_ID = "amy"

auth = base64.b64encode(DID_KEY.encode("ascii")).decode("ascii")
headers = {
    "Authorization": f"Basic {auth}",
    "accept": "application/json",
    "content-type": "application/json"
}

def create_talk_with_embedded_audio():
    if not os.path.exists(AUDIO_FILE):
        print("Audio file not found:", AUDIO_FILE)
        sys.exit(1)

    with open(AUDIO_FILE, "rb") as f:
        audio_bytes = f.read()
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    url = "https://api.d-id.com/talks"
    payload = {
        "presenter_id": PRESENTER_ID,
        "script": {
            "type": "audio",
            "audio": audio_b64
        },
        "config": {
            "fluent": False,
            "pad_audio": 0,
            "show_watermark": False
        }
    }

    r = requests.post(url, headers=headers, json=payload)
    if r.status_code not in (200, 201):
        print("Talk creation failed:", r.status_code, r.text)
        sys.exit(1)
    talk_id = r.json().get("id")
    print("Talk created:", talk_id)
    return talk_id

def poll_talk(talk_id):
    url = f"https://api.d-id.com/talks/{talk_id}"
    while True:
        r = requests.get(url, headers=headers)
        data = r.json()
        status = data.get("status", "")
        print("Status:", status)
        if status in ("done", "finished", "succeeded"):
            return data.get("result_url")
        elif status in ("error", "failed", "rejected"):
            print("Talk failed:", data)
            sys.exit(1)
        time.sleep(2)

def download_video(video_url):
    r = requests.get(video_url, stream=True)
    if r.status_code != 200:
        print("Download failed:", r.status_code, r.text)
        sys.exit(1)
    with open(OUTPUT_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("Saved video as:", OUTPUT_FILE)

def main():
    talk_id = create_talk_with_embedded_audio()
    video_url = poll_talk(talk_id)
    print("Video ready:", video_url)
    download_video(video_url)

if __name__ == "__main__":
    main()
