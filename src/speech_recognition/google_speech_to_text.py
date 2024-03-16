from google.cloud import speech
from google.oauth2 import service_account

class GoogleSpeechToText:
    def __init__(self, credentials_path):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = speech.SpeechClient(credentials=self.credentials)

    def transcribe(self, audio_file_path):
        """Transcribe the given audio file to text."""
        with open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
            audio_channel_count = 2
        )

        response = self.client.recognize(config=config, audio=audio)

        # Concatenate the results from the multiple portions of the audio file
        transcript = ' '.join(result.alternatives[0].transcript for result in response.results)
        
        return transcript
