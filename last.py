import requests
import time
import base64
import os

# ===== CONFIG =====
DID_KEY = "YmFua3Byb2NvaW5AZ21haWwuY29t:T5WmlTQYwBpQ1NlTBy17k"
AUDIO_FILE = "silence5s.mp3"
OUTPUT_FILE = "amy_silent.mp4"
PRESENTER_ID = "amy"
# ==================

auth = base64.b64encode(DID_KEY.encode("ascii")).decode("ascii")
headers = {
    "Authorization": f"Basic {auth}",
    "accept": "application/json"
}


def upload_audio():
    if not os.path.exists(AUDIO_FILE):
        print("Audio file not found:", AUDIO_FILE)
        raise SystemExit

    print("Uploading silent audio...")
    url = "https://api.d-id.com/audios"
    files = {
        "audio": (AUDIO_FILE, open(AUDIO_FILE, "rb"), "audio/mpeg")
    }
    r = requests.post(url, files=files, headers=headers)
    if r.status_code not in (200, 201):
        print("Audio upload failed:", r.status_code, r.text)
        raise SystemExit
    data = r.json()
    print("Uploaded successfully:", data["url"])
    return data["url"]


def create_talk(audio_url):
    url = "https://api.d-id.com/talks"
    payload = {
        "presenter_id": PRESENTER_ID,
        "script": {
            "type": "audio",
            "audio_url": audio_url
        },
        "config": {
            "pad_audio": 0,
            "stitch": False,
            "fluent": False,
            "show_watermark": False
        }
    }

    r = requests.post(url, headers={**headers, "Content-Type": "application/json"}, json=payload)
    if r.status_code not in (200, 201):
        print("Talk creation failed:", r.status_code, r.text)
        raise SystemExit
    data = r.json()
    print("Talk created:", data["id"])
    return data["id"]


def poll_talk(talk_id):
    url = f"https://api.d-id.com/talks/{talk_id}"
    while True:
        r = requests.get(url, headers=headers)
        data = r.json()
        status = data.get("status", "").lower()
        print("Status:", status)
        if status in ("done", "finished", "succeeded"):
            return data.get("result_url")
        elif status in ("failed", "error", "rejected"):
            print("Talk failed:", data)
            raise SystemExit
        time.sleep(2)


def download_video(video_url):
    r = requests.get(video_url, stream=True)
    if r.status_code != 200:
        print("Download failed:", r.status_code, r.text)
        raise SystemExit
    with open(OUTPUT_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("Saved video as:", OUTPUT_FILE)


def main():
    audio_url = upload_audio()
    talk_id = create_talk(audio_url)
    video_url = poll_talk(talk_id)
    print("Video ready:", video_url)
    download_video(video_url)


if __name__ == "__main__":
    main()
