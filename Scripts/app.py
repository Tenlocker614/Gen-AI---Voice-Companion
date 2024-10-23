import tkinter as tk
from tkinter import messagebox
import pyaudio
import numpy as np
import wave
import speech_recognition as sr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class AudioRecorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 44100
        self.frames = []
        self.p = pyaudio.PyAudio()

        # Set up the plot
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2, color='cyan')
        self.ax.set_xlim(0, self.chunk / self.fs)
        self.ax.set_ylim(-32768, 32767)
        self.ax.set_title("Real-Time Audio Waveform",
                          fontsize=20, fontweight='bold')
        self.ax.set_xlabel("Time (s)", fontsize=14)
        self.ax.set_ylabel("Amplitude", fontsize=14)
        self.ax.grid(color='lightgray', linestyle='--', linewidth=0.5)
        self.ax.set_facecolor('#282c34')

        # Create a background for the plot
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

    def start_recording(self):
        self.frames = []
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)

        self.ani = FuncAnimation(
            self.fig, self.update_plot, frames=self.get_audio_data, blit=True)
        plt.show()

    def get_audio_data(self):
        while True:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            yield np.frombuffer(data, dtype=np.int16)

    def update_plot(self, data):
        self.line.set_ydata(data)
        self.line.set_xdata(np.linspace(
            0, self.chunk / self.fs, num=self.chunk))
        return self.line,

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        # Save the recorded data
        wave_file = wave.open("temp_audio.wav", 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.p.get_sample_size(self.sample_format))
        wave_file.setframerate(self.fs)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

        # Transcribe the audio
        self.transcribe_audio()

    def transcribe_audio(self):
        audio_file = "temp_audio.wav"
        with sr.AudioFile(audio_file) as source:
            audio_data = self.recognizer.record(source)
            try:
                transcript = self.recognizer.recognize_google(audio_data)
                messagebox.showinfo("Transcription", transcript)
            except sr.UnknownValueError:
                messagebox.showerror(
                    "Error", "Could not understand the audio.")
            except sr.RequestError:
                messagebox.showerror(
                    "Error", "Could not request results from Google Speech Recognition service.")


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder and Transcriber")
        self.recorder = AudioRecorder()

        self.start_button = tk.Button(
            master, text="Start Recording", command=self.start_recording, bg='cyan', fg='black', font=('Arial', 14))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            master, text="Stop Recording", command=self.stop_recording, bg='cyan', fg='black', font=('Arial', 14))
        self.stop_button.pack(pady=10)

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.recorder.start_recording()

    def stop_recording(self):
        self.start_button.config(state=tk.NORMAL)
        self.recorder.stop_recording()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
