import threading
from speech_recognition.google_speech_to_text import GoogleSpeechToText
from command_interpreter.t5 import T5CommandInterpreter
from audio_capture.microphone import AudioRecorder
from command_interpreter.gpt4 import GPT4CommandInterpreter
from fast_downward_wrapper.wrapper import FastDownwardWrapper

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

    if option == '1' or option == '2':
        # Path to your Google Cloud credentials JSON file
        credentials_path = 'google-credentials.json'
        
        # Initialize the speech-to-text service
        stt_service = GoogleSpeechToText(credentials_path=credentials_path)
        
        # Transcribe the audio file
        transcript = stt_service.transcribe(audio_file_path)
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

if __name__ == '__main__':
    main()