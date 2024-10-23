# GenAI Voice Companion

The **GenAI Voice Companion** is a Python-based application that records your voice, transcribes it to text, and visualizes the real-time audio waveform. It leverages libraries such as `pyaudio` and `speech_recognition` for capturing and transcribing audio, and `wave` and `matplotlib` for analyzing and visualizing the waveform. The interface is built using `Streamlit`, providing an intuitive and interactive user experience.

## Features

- **Voice Recording**: Capture real-time voice input from your microphone.
- **Voice Transcription**: Automatically transcribe the recorded voice into text.
- **Waveform Visualization**: Analyze and display the real-time waveform of the recorded audio.
- **Interactive Interface**: Visualize audio data and view transcriptions via an easy-to-use `Streamlit` interface.

## Functional Requirements

1. **Voice Recording**:  
   Capture audio from the user's microphone using the `pyaudio` library.

2. **Speech Transcription**:  
   Convert the captured audio to text using the `speech_recognition` library.

3. **Waveform Analysis**:  
   Extract and analyze waveform data from the recorded audio using the `wave` library.

4. **Real-Time Waveform Visualization**:  
   Visualize the waveform of the recorded audio in real time using `matplotlib`.

5. **User Interface**:  
   Display the transcription and waveform in an interactive `Streamlit` web app.

## Non-Functional Requirements

- **Performance**: Real-time audio processing with minimal delay.
- **Usability**: Simple and intuitive interface for ease of use.
- **Scalability**: Designed to support single-user interactions but can be expanded.
- **Security**: Audio data is processed locally; no data is stored or transmitted without user consent.
- **Portability**: Cross-platform compatibility (Windows, macOS, Linux).

## Tech Stack

- **Languages**: Python
- **Libraries**:
  - `pyaudio`: For capturing audio through the microphone.
  - `speech_recognition`: For transcribing speech to text.
  - `wave`: For audio analysis.
  - `matplotlib`: For waveform visualization.
  - `streamlit`: For building the web interface.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Tenlocker614/GenAI---Voice-Companion.git

2. **Run the application: Start the Streamlit application by running the following command:**
    ```bash
    streamlit run app-streamlit.py

## Usage

1. **Recording Voice:**
    - Once the application is open in your browser, press the "Record" button to start recording your voice through your microphone.
2. **Viewing Transcription:**
   - The app will automatically transcribe your voice into text and display the transcription on the screen
3. **Waveform Visualization:**
   - Simultaneously, a real-time waveform of your voice will be shown on the app's interface using the matplotlib visualization tool.
4. **Stop Recording:**
   - Click the "Stop" button to end the recording and view the complete transcription and waveform.
  
## Dependencies
Ensure that the following dependencies are installed to run the GenAI Voice Companion application:
- Python 3.8+: The code is compatible with Python versions 3.8 and above.
- pyaudio: For capturing audio input from the microphone.
- speech_recognition: To transcribe the recorded audio into text.
- wave: For analyzing the waveform of the recorded audio.
- matplotlib: For real-time waveform visualization.
- streamlit: To create the user-friendly web application interface.
