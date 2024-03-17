<p align="center">
  <img width="100" src="https://images.squarespace-cdn.com/content/v1/5ab0712975f9ee24a7be79df/1537854791575-E0EOCBCKSCNDDMY8Z0P1/TIAGo+with+hey5+hand.png">
</p>

# TIAGo-NLUI Project

TIAGo-NLUI (Natural Language User Interface for the TIAGo robot) is a software framework designed to empower the TIAGo robot by PAL Robotics with the ability to interpret and execute commands given in natural language. This project leverages speech recognition and natural language processing (NLP) technologies to enhance human-robot interaction.

## Features

- **Speech Recognition**: Utilizes Google's Speech-to-Text API to accurately convert spoken language into text.
- **Command Interpretation**: Employs the T5 transformer model for understanding the intent behind the transcribed text and mapping it to specific robot actions.
- **Audio Capture Options**: Offers flexibility in command input through live audio recording from a microphone or processing pre-recorded audio files.
- **Modular Design**: Facilitates easy extension and customization for different languages, commands, and actions, catering to a wide range of applications and user needs.

## Getting Started

### Prerequisites

- Python 3.8 or newer
- Access to Google Cloud Speech-to-Text API
- Pip for Python package installation

### Installation

1. **Clone the Repository**

   ```
   git clone https://github.com/SamSeban/TIAGo-NLUI.git
   cd TIAGo-NLUI
   ```

2. **Install Required Python Packages**

   ```
   pip install -r requirements.txt
   ```

3. **Google Cloud Speech-to-Text Setup**

   - Ensure you have a Google Cloud account with the Speech-to-Text API enabled.
   - Download your API key JSON file and place it in the project directory.

### Usage

Run the `main.py` script to start the application:

```
python main.py
```

Follow the on-screen prompts to choose between transcribing from an audio file or recording a new command through the microphone.

### Configuration

- **API Key**: Update the `credentials_path` in `main.py` to the location of your Google Cloud Speech-to-Text API key JSON file.
- **Model Selection**: The default model used for command interpretation is `t5-small`. It can be changed to any other T5 model variant as needed for your specific requirements.


## License

This project is licensed under the MIT License.
