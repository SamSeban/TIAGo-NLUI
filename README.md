<p align="center">
  <img width="100" src="https://images.squarespace-cdn.com/content/v1/5ab0712975f9ee24a7be79df/1537854791575-E0EOCBCKSCNDDMY8Z0P1/TIAGo+with+hey5+hand.png">
</p>

# TIAGo-NLUI Project

TIAGo-NLUI (Natural Language User Interface for the TIAGo robot) is a software framework designed to empower the TIAGo robot by PAL Robotics with the ability to interpret and execute commands given in natural language. This project leverages speech recognition and natural language processing (NLP) technologies to enhance human-robot interaction.

## Features

- **Audio Capture Options**: Offers flexibility in command input through live audio recording from a microphone or processing pre-recorded audio files.
- **Speech Recognition**: Utilizes Google's Speech-to-Text API to accurately convert spoken language into text.
- **Command Interpretation**: Employs GPT4 model for understanding the intent behind the transcribed text and mapping it to a specific PDDL format problem.


## Getting Started

### Prerequisites

- Python 3.8 or newer
- Access to Google Cloud Speech-to-Text API
- Access to OpenAI GPT4 API
- Pip for Python package installation
- `cmake` (required for building Fast Downward)

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

4. **GPT4 API Setup**

   - Ensure you have an OpenAI account with a GPT API key.
   - Create a openai-credentials.json file with your API key in an "api-key" field and place it in the project directory.

5. **Fast Downward Setup**

Fast Downward is used for planning tasks within the framework. Follow these steps to set it up:

- Make sure you have `cmake` installed on your system.
- Navigate to the Fast Downward directory:
  
  ```
  cd external/fast_downward
  ```
  
- Build Fast Downward using the release configuration:
  
  ```
  ./build.py release
  ```

### Usage

Run the `main.py` script to start the application:

```
python main.py
```

Follow the on-screen prompts to transcribe natural language to a PDDL plan.

### Configuration

- **Google API Key**: Update the `credentials_path` in `main.py` to the location of your Google Cloud Speech-to-Text API key JSON file.


## License

This project is licensed under the MIT License.
