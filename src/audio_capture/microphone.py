import threading
import pyaudio
import wave

class AudioRecorder:
    def __init__(self, file_path="live_audio.wav"):
        self.file_path = file_path
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.sample_rate = 44100
        self.recording = False
        self.frames = []

    def start_recording(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)
        self.recording = True
        self.frames = []
        print("Recording started. Press Enter to stop.")
        
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
        wf = wave.open(self.file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        print("Recording stopped and file saved.")