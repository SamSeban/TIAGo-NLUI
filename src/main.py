from speech_recognition.google_speech_to_text import GoogleSpeechToText

def main():
    # Path to your Google Cloud credentials JSON file
    credentials_path = 'google-credentials.json'
    
    # Initialize the speech-to-text service
    stt_service = GoogleSpeechToText(credentials_path=credentials_path)
    
    # Path to the audio file you want to transcribe
    audio_file_path = 'path/to/your/audiofile.wav'
    
    # Transcribe the audio file
    transcript = stt_service.transcribe(audio_file_path)
    print("Transcription: ", transcript)

if __name__ == '__main__':
    main()
