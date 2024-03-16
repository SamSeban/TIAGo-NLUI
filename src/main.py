from speech_recognition.google_speech_to_text import GoogleSpeechToText
from command_interpreter.t5 import T5CommandInterpreter

def main():
    # Path to your Google Cloud credentials JSON file
    credentials_path = 'google-credentials.json'
    
    # Initialize the speech-to-text service
    stt_service = GoogleSpeechToText(credentials_path=credentials_path)
    
    # Path to the audio file you want to transcribe
    audio_file_path = '/home/sam/Documents/Technion/Semester 7/Philosophy of Time and Space/Writing Assignment 2/first.wav'
    
    # Transcribe the audio file
    transcript = stt_service.transcribe(audio_file_path)
    print("Transcription: ", transcript)

    interpreter = T5CommandInterpreter(model_name="t5-small")
    interpreted_command = interpreter.interpret_command(transcript)
    print(f"Interpreted Command: {interpreted_command}")



if __name__ == '__main__':
    main()
