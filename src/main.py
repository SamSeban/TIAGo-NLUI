import threading
import wave
import subprocess
from speech_recognition.google_speech_to_text import GoogleSpeechToText
from command_interpreter.t5 import T5CommandInterpreter
from audio_capture.microphone import AudioRecorder
from command_interpreter.gpt4 import GPT4CommandInterpreter
from fast_downward_wrapper.wrapper import FastDownwardWrapper
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename  
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'wav'}

def record_audio_on_demand():
    recorder = AudioRecorder()
    recording_thread = threading.Thread(target=recorder.start_recording)
    recording_thread.start()
    input("Press Enter to stop the recording...\n")
    recorder.stop_recording()
    return recorder.file_path

def main():
    print("Select an option:\n1. Transcribe from a specific audio file\n2. Record and transcribe from the microphone\n3. Send a written command")
    option = input("Option: ")
    print("Select an interpreter:\n1. GPT4\n2. T5")
    interpreter_opt = input("Option: ")

    if option == '1':
        audio_file_path = input("Enter the path to the audio file: ")
    elif option == '2':
        audio_file_path = record_audio_on_demand()
    elif option == '3':
        transcript = input("Write the natural language command: ")
    else:
        print("Invalid option.")
        return
    channels = 1
    if option == '1' or option == '2':
        # Path to your Google Cloud credentials JSON file
        credentials_path = 'google-credentials.json'
        
        # Initialize the speech-to-text service
        stt_service = GoogleSpeechToText(credentials_path=credentials_path)

        if option == '1':
            command = ['ffmpeg', '-i', 'recording.mp4', '-vn', '-ar', 44100, '-ac', 2, '-b:a', '192k', 'recording.mp3']
            subprocess.run(command, check=True)

        if option == '2':
            with wave.open(audio_file_path, 'rb') as wf:
                channels = wf.getnchannels()

        # Transcribe the audio file
        transcript = stt_service.transcribe(audio_file_path, channels)
        print("Transcription: ", transcript)

    if interpreter_opt == '1':
        interpreter = GPT4CommandInterpreter()
        prompt = interpreter.create_prompt(transcript)
        interpreted_command = interpreter.send_prompt(prompt)
    elif interpreter_opt == '2':
        interpreter = T5CommandInterpreter()
        interpreted_command = interpreter.interpret_command(transcript)
    else:
        print("Invalid option.")

    fd_wrapper = FastDownwardWrapper()
    solution = fd_wrapper.solve(interpreted_command)
    print("Plan found:\n", solution)

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.form
    option = data['option']
    interpreter_opt = data['interpreter']

    command_text = ""
    filename = ""

    channels = 1
    
    if option == '1' or option == '2':
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file"}), 400
        filename = secure_filename(file.filename)
        audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(audio_file_path)

        # Path to your Google Cloud credentials JSON file
        credentials_path = 'google-credentials.json'

        # Initialize the speech-to-text service
        stt_service = GoogleSpeechToText(credentials_path=credentials_path)
        if option == '2':
            with wave.open(audio_file_path, 'rb') as wf:
                channels = wf.getnchannels()

        # Transcribe the audio file
        command_text = stt_service.transcribe(audio_file_path, channels, option)
    elif option == '3':
        command_text = data.get('commandText', '')
    print("Transcript: ", command_text)
    # Initialize the appropriate command interpreter based on user selection
    if interpreter_opt == '1':
        interpreter = GPT4CommandInterpreter()
        prompt = interpreter.create_prompt(command_text)
        interpreted_command = interpreter.send_prompt(prompt)
    elif interpreter_opt == '2':
        interpreter = T5CommandInterpreter()
        interpreted_command = interpreter.interpret_command(command_text)
    else:
        return jsonify({"error": "Invalid interpreter option"}), 400
    print("Interpreted: ", interpreted_command)

    fd_wrapper = FastDownwardWrapper() 
    solution = fd_wrapper.solve(interpreted_command)
    print("Solution: ", solution)

    return jsonify({
        "transcript": command_text,
        "interpretedCommand": interpreted_command,
        "solution": solution
    })


if __name__ == '__main__': 
    #main()
    app.run(host='0.0.0.0', debug=True)