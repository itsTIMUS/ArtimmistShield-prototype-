import cv2
import pyaudio
import wave
import serial
import time
import smbus
import threading
import platform
from datetime import datetime

# Detect platform (Raspberry Pi or Windows)
is_raspberry_pi = platform.system() == "Linux"

# GPS Module (NEO-6M)
if is_raspberry_pi:
	gps_serial = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
else:
	gps_serial = None # Mock GPS for Windows

def get_gps_data():
	"""Fetch GPS coordinates from the NEO-6M module."""
	if not is_raspberry_pi:
		return "22.5726 N, 88.3639 E" # Mock location (Kolkata, India)
	while True:
		try:
			line = gps_serial.readline().decode('utf-8', errors='ignore')
			if "$GPGGA" in line:
				data = line.split(",")
				if len(data) > 4 and data[2] and data[4]:
					lat = float(data[2]) / 100
					lon = float(data[4]) / 100
					return f"{lat} N, {lon} E"
		except Exception as e:
			return "GPS Error"

# MPU-6050 Configuration
if is_raspberry_pi:
	bus = smbus.SMBus(1)
	MPU_ADDR = 0x68
	bus.write_byte_data(MPU_ADDR, 0x6B, 0)
else:
	bus = None # Mock MPU-6050 for Windows

def read_mpu():
	"""Read acceleration data from MPU-6050 and detect fall."""
	if not is_raspberry_pi:
		return (0, 0, 9.8) # Mock values
	accel_x = bus.read_byte_data(MPU_ADDR, 0x3B)
	accel_y = bus.read_byte_data(MPU_ADDR, 0x3D)
	accel_z = bus.read_byte_data(MPU_ADDR, 0x3F)
	return (accel_x, accel_y, accel_z)

def detect_fall():
	"""Detect fall using acceleration data."""
	while True:
		x, y, z = read_mpu()
		if z < 3: # Simple threshold for fall detection
			print("Fall Detected! Sending Emergency Alert...")
			# Implement emergency alert here
		time.sleep(1)

def record_video():
	"""Record video using the OV5647 camera (or laptop webcam)."""
	cap = cv2.VideoCapture(0)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter(f'video_{datetime.now().strftime("%Y%m%d_%H%M%S")}.avi', fourcc, 20.0, (640, 480))
	start_time = time.time()
	while time.time() - start_time < 60:
		ret, frame = cap.read()
		if ret:
			out.write(frame)
			cv2.imshow('Recording', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
	cap.release()
	out.release()
	cv2.destroyAllWindows()

def record_audio():
	"""Record audio using a USB microphone (or laptop mic)."""
	chunk = 1024
	sample_format = pyaudio.paInt16
	channels = 1
	rate = 44100
	p = pyaudio.PyAudio()
	stream = p.open(format=sample_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
	frames = []
	start_time = time.time()
	while time.time() - start_time < 60:
		data = stream.read(chunk)
		frames.append(data)
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open(f'audio_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav', 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(rate)
	wf.writeframes(b''.join(frames))
	wf.close()

def main():
	"""Main function to start video, audio, and fall detection."""
	print("Starting Women Safety Device...")

	gps_thread = threading.Thread(target=get_gps_data)
	gps_thread.start()

	fall_thread = threading.Thread(target=detect_fall)
	fall_thread.start()

	video_thread = threading.Thread(target=record_video)
	video_thread.start()

	audio_thread = threading.Thread(target=record_audio)
	audio_thread.start()

	gps_thread.join()
	fall_thread.join()
	video_thread.join()
	audio_thread.join()

	print("Recording completed.")

if __name__ == "__main__":
	main()
