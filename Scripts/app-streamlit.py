import streamlit as st
import speech_recognition as sr
import wave
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tempfile
import os


class Companion:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 400

    def record_audio(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            st.write("Listening...")
            audio = self.recognizer.listen(source)

            # Save the audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                wav_data = audio.get_wav_data()
                tmp_file.write(wav_data)
                audio_file_path = tmp_file.name

        st.write("Stopped Listening...")
        return audio_file_path, self.recognizer.recognize_google(audio)


def plot_waveform(audio_data, frame_rate):
    # Create time axis for plotting
    n_frames = len(audio_data)
    time = np.linspace(0, n_frames / frame_rate, num=n_frames)

    # Create a figure for the waveform
    fig, ax = plt.subplots()
    ax.set_xlim(0, time[-1])
    ax.set_ylim(-32768, 32767)

    line, = ax.plot([], [], lw=2, color='skyblue')
    ax.set_title("Real-Time Audio Waveform", fontsize=16, fontweight='bold')
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Amplitude", fontsize=12)
    ax.grid(color='lightgray', linestyle='--', linewidth=0.5)

    return fig, ax, line, time


def main():
    st.title("🎤 Audio Recorder and Transcriber")
    st.markdown("""
    This app allows you to record audio and transcribe it into text. 
    Click the button below to start recording your voice!
    """)

    companion = Companion()

    if st.button("Start Recording"):
        audio_file_path, transcript = companion.record_audio()

        # Read the audio data from the temporary file
        with wave.open(audio_file_path, 'rb') as wf:
            n_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            frame_rate = wf.getframerate()
            n_frames = wf.getnframes()
            frames = wf.readframes(n_frames)

        # Convert to numpy array
        audio_data = np.frombuffer(frames, dtype=np.int16)

        # Plot the waveform in real-time
        fig, ax, line, time = plot_waveform(audio_data, frame_rate)
        st.pyplot(fig)

        # Display the transcribed text with styling
        st.subheader("Transcription:", anchor='transcription')
        st.markdown(
            f"<div style='font-size: 24px; font-family: Arial; color: #4CAF50; background-color: #f9f9f9; padding: 10px; border-radius: 5px;'>{transcript}</div>", unsafe_allow_html=True)

        # Clean up the temporary file
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)


if __name__ == "__main__":
    main()
