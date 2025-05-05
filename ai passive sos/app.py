import time
import requests
import smtplib
import streamlit as st
import sounddevice as sd
import numpy as np
import wave
from email.mime.text import MIMEText
from threading import Thread

# === AssemblyAI Configuration ===
ASSEMBLYAI_API_KEY = "your_key"  # Replace with your actual AssemblyAI API key
ASSEMBLYAI_UPLOAD_URL = "upload_url"
ASSEMBLYAI_TRANSCRIPT_URL = "transcript_url"

# === Audio Configuration ===
SAMPLE_RATE = 44100       # in Hz
CHANNELS = 1              # mono audio
CHUNK_DURATION = 5        # seconds per audio chunk
AUDIO_FILENAME = "temp_chunk.wav"

# === Distress Keywords ===
DISTRESS_KEYWORDS = {"help", "sos", "emergency", "911", "save me", "distress", "assistance", "trapped", "danger"}

# --- Custom CSS for Beautiful UI ---
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .header {
        font-size: 2.5em;
        color: #4B0082;
        font-weight: bold;
        text-align: center;
    }
    .subheader {
        font-size: 1.2em;
        color: #3124;
        text-align: center;
    }
    .section {
        background-color: #gggggg;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0.1,0.1);
        margin-bottom: 20px;
    }
    .btn {
        background-color: #4B0082;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .btn:hover {
        background-color: #6A0DAD;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Page Title and Description ---
st.markdown('<div class="header">AI Passive SOS</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Passive Listening. Automatic Alerts. Enhanced Safety.</div>', unsafe_allow_html=True)
st.write("This system continuously listens to your audio, transcribes it using AssemblyAI, and sends an SOS alert if distress keywords are detected.")

# --- Email Configuration Section ---
st.markdown('<div class="section"><h3>Email Configuration</h3></div>', unsafe_allow_html=True)
with st.container():
    email_username = st.text_input("📧 Enter your Email (Sender)", "")
    email_password = st.text_input("🔑 Enter your Email Password (App Password)", "", type="password")
    recipient_email = st.text_input("📩 Enter Recipient Email for SOS Alerts:", "")

# --- Global flag for continuous recording ---
recording = False
stop_due_to_distress = False

def save_audio_chunk(audio_chunk, filename=AUDIO_FILENAME):
    """Save a numpy audio chunk to a WAV file."""
    audio_int16 = (audio_chunk * 32767).astype(np.int16)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit audio = 2 bytes
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())
    st.info(f"✅ Audio chunk saved as {filename}")

def upload_audio(file_path):
    """Upload audio file to AssemblyAI and return the audio URL."""
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    with open(file_path, "rb") as f:
        response = requests.post(ASSEMBLYAI_UPLOAD_URL, headers=headers, data=f)
    response.raise_for_status()
    st.info("🔄 Audio chunk uploaded to AssemblyAI.")
    return response.json()['upload_url']

def request_transcription(audio_url):
    """Request transcription from AssemblyAI."""
    headers = {"authorization": ASSEMBLYAI_API_KEY, "content-type": "application/json"}
    json_data = {"audio_url": audio_url}
    response = requests.post(ASSEMBLYAI_TRANSCRIPT_URL, json=json_data, headers=headers)
    response.raise_for_status()
    st.info("⏳ Transcription requested...")
    return response.json()['id']

def poll_transcription(transcript_id):
    """Poll AssemblyAI API until transcription is complete and return the text."""
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    polling_url = f"{ASSEMBLYAI_TRANSCRIPT_URL}/{transcript_id}"
    while True:
        response = requests.get(polling_url, headers=headers)
        response.raise_for_status()
        status = response.json()['status']
        if status == 'completed':
            st.info("✅ Transcription completed.")
            return response.json()['text']
        elif status == 'error':
            raise Exception("Error in transcription")
        time.sleep(3)

def contains_distress(text):
    """Check if the transcript contains any distress keywords."""
    text_lower = text.lower()
    for keyword in DISTRESS_KEYWORDS:
        if keyword in text_lower:
            st.error(f"🚨 Detected distress keyword: {keyword}")
            return True
    return False

def send_alert_email(transcript_text):
    """Send an SOS alert email with the transcript text."""
    if not (email_username and email_password and recipient_email):
        st.warning("⚠️ Please enter all email credentials before sending an alert.")
        return

    subject = "🚨 SOS Alert: Distress Detected!"
    body = f"A distress keyword was detected in a recent transcription:\n\n{transcript_text}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_username
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_username, email_password)
            server.sendmail(email_username, recipient_email, msg.as_string())
        st.success("✅ SOS Alert email sent successfully!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")

def process_audio_chunk(audio_chunk):
    """Process a single audio chunk: save, transcribe, detect distress, and send an alert if needed."""
    global stop_due_to_distress
    save_audio_chunk(audio_chunk)
    try:
        audio_url = upload_audio(AUDIO_FILENAME)
        transcript_id = request_transcription(audio_url)
        transcript_text = poll_transcription(transcript_id)
        st.markdown(f"### 📝 Chunk Transcription:\n{transcript_text}")
        if contains_distress(transcript_text):
            st.warning("🚨 Distress keywords detected! Sending SOS alert message.")
            send_alert_email(transcript_text)
            stop_due_to_distress = True
    except Exception as e:
        st.error(f"❌ Error processing audio chunk: {e}")

def continuous_recording():
    """Continuously record audio in CHUNK_DURATION segments and process each chunk.
       Automatically stop if a distress keyword is detected."""
    global recording, stop_due_to_distress
    st.info("🎤 Continuous Recording Started...")
    recording = True
    stop_due_to_distress = False

    audio_buffer = []  # buffer for audio chunks
    start_time = time.time()

    # Callback to collect audio data
    def audio_callback(indata, frames, time_info, status):
        audio_buffer.append(indata.copy())

    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback)
    stream.start()

    while recording:
        if time.time() - start_time >= CHUNK_DURATION:
            stream.stop()
            if audio_buffer:
                chunk_data = np.concatenate(audio_buffer, axis=0)
                st.info("Processing audio chunk...")
                process_audio_chunk(chunk_data)
                audio_buffer.clear()
                start_time = time.time()
            # If distress was detected, stop recording automatically.
            if stop_due_to_distress:
                st.warning("⛔ Distress detected! Stopping continuous recording.")
                recording = False
                break
            stream.start()  # Resume recording

    stream.stop()
    stream.close()
    st.info("🛑 Continuous Recording Stopped.")

# --- Button Section ---
st.markdown('<div class="section"><h3>Control Panel</h3></div>', unsafe_allow_html=True)
if st.button("🎙️ Start Passive SOS", key="start"):
    if not (email_username and email_password and recipient_email):
        st.warning("⚠️ Please fill in all email credentials before starting.")
    else:
        Thread(target=continuous_recording).start()

