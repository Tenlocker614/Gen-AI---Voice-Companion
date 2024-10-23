import sys
import wave
import numpy as np
import pyaudio
import speech_recognition as sr
from PyQt5 import QtWidgets, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AudioRecorder(QtCore.QObject):
    update_plot_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 44100
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None

        self.update_plot_signal.connect(self.update_plot)

    def start_recording(self):
        self.frames = []
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)

        self.recording = True
        self.record_audio()

    def record_audio(self):
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.int16)
            self.update_plot_signal.emit(audio_data)

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wave_file = wave.open("temp_audio.wav", 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.p.get_sample_size(self.sample_format))
        wave_file.setframerate(self.fs)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

        self.transcribe_audio()

    def transcribe_audio(self):
        audio_file = "temp_audio.wav"
        with sr.AudioFile(audio_file) as source:
            audio_data = self.recognizer.record(source)
            try:
                transcript = self.recognizer.recognize_google(audio_data)
                QtWidgets.QMessageBox.information(
                    None, "Transcription", transcript)
            except sr.UnknownValueError:
                QtWidgets.QMessageBox.critical(
                    None, "Error", "Could not understand the audio.")
            except sr.RequestError:
                QtWidgets.QMessageBox.critical(
                    None, "Error", "Could not request results from Google Speech Recognition service.")

    def update_plot(self, data):
        self.canvas.plot_waveform(data)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.ax.set_title("Real-Time Audio Waveform",
                          fontsize=16, fontweight='bold')
        self.ax.set_xlabel("Samples", fontsize=12)
        self.ax.set_ylabel("Amplitude", fontsize=12)
        self.ax.grid(color='lightgray', linestyle='--', linewidth=0.5)
        self.ax.set_ylim(-32768, 32767)
        self.line, = self.ax.plot([], [], lw=2, color='cyan')
        self.xdata = np.arange(0, 1024)

    def plot_waveform(self, data):
        self.line.set_ydata(data)
        self.line.set_xdata(self.xdata)
        self.draw()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.recorder = AudioRecorder()
        self.recorder.canvas = PlotCanvas(self)

        self.start_button = QtWidgets.QPushButton("Start Recording")
        self.stop_button = QtWidgets.QPushButton("Stop Recording")
        self.stop_button.setEnabled(False)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.recorder.canvas)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.recorder.start_recording()

    def stop_recording(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.recorder.stop_recording()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Audio Recorder and Transcriber")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
