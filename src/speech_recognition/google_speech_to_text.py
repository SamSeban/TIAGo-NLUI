from google.cloud import speech
from google.oauth2 import service_account

class GoogleSpeechToText:
    def __init__(self, credentials_path):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = speech.SpeechClient(credentials=self.credentials)

    def transcribe(self, audio_file_path, channels, option):
        """Transcribe the given audio file to text."""    
        with open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()

        if option == '1':
            encoding = None
        elif option == '2':
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=encoding,
            language_code="en-US",
            audio_channel_count = channels
        )

        response = self.client.recognize(config=config, audio=audio)

        # Concatenate the results from the multiple portions of the audio file
        transcript = ' '.join(result.alternatives[0].transcript for result in response.results)
        return transcript