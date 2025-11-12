import subprocess, requests, base64, time, json, pathlib

DID_KEY = "YmFua3Byb2NvaW5AZ21haWwuY29t:T5WmlTQYwBpQ1NlTBy17k"
PRESENTER_ID = "amy-jcwCkr1grs"

SILENCE_FILE = pathlib.Path("silence5s.mp3")
VIDEO_FILE = pathlib.Path("avatar_alive_quiet.mp4")

# --- make 5 s of silence directly with FFmpeg ---
subprocess.run([
    "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
    "-t", "5", "-q:a", "9", "-acodec", "libmp3lame", str(SILENCE_FILE)
], check=True)

# --- send to D-ID ---
with open(SILENCE_FILE, "rb") as f:
    encoded_audio = base64.b64encode(f.read()).decode()

auth = base64.b64encode(DID_KEY.encode()).decode()
headers = {
    "Authorization": f"Basic {auth}",
    "accept": "application/json",
    "content-type": "application/json"
}
payload = {
    "script": {"type": "audio", "audio_base64": encoded_audio},
    "presenter_id": PRESENTER_ID,
    "config": {"fluent": True}
}

res = requests.post("https://api.d-id.com/talks", headers=headers, json=payload)
if res.status_code != 201:
    print("Error creating talk:", res.status_code, res.text)
    raise SystemExit
talk_id = res.json()["id"]

status_url = f"https://api.d-id.com/talks/{talk_id}"
while True:
    r = requests.get(status_url, headers=headers).json()
    if r.get("status") == "done":
        video_url = r["result_url"]
        print("Video ready:", video_url)
        break
    elif r.get("status") == "error":
        print("Error:", r)
        raise SystemExit
    time.sleep(3)

video_data = requests.get(video_url).content
VIDEO_FILE.write_bytes(video_data)
print("Saved:", VIDEO_FILE)