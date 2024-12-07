import tkinter as tk
import speech_recognition as sr
import pyaudio
import wave
import threading
import os


# Global variables
recording = False
audio_frames = []


def start_recording():
    global recording
    recording = True
    threading.Thread(target=record_audio).start()


def stop_recording():
    global recording
    recording = False


def record_audio():
    global recording, audio_frames
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
    print('Recording')
    audio_frames = []
    while recording:
        data = stream.read(chunk)
        audio_frames.append(data)
    print('Finished recording')

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the audio file
    output_dir = r'enter your output path'  # Assuming this is the directory
    filename = os.path.join(output_dir, "output.wav")
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(audio_frames))
    wf.close()


def convert_audio_to_text():
    output_dir = r'enter your output path'
    filename = os.path.join(output_dir, "output.wav")
    speech_to_text(filename, output_dir)
    


def speech_to_text(audio_file, output_dir):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)

    try:
        text = r.recognize_google(audio_data)
        txtSpeech.insert(tk.END, text + "\n")

        # Save the text to a file with proper newline handling
        txt_file = os.path.join(output_dir, "output.txt")
        with open(txt_file, "w", encoding="utf-8") as file:
            file.write(text)

    except sr.UnknownValueError:
        txtSpeech.insert(tk.END, "Could not understand audio\n")
    except sr.RequestError as e:
        txtSpeech.insert(tk.END, "Error: {0}\n".format(e))


def reset():
    txtSpeech.delete('1.0', tk.END)  # Clear the text box

    # Clear the output file
    output_dir = r'enter your output path'
    txt_file = os.path.join(output_dir, "output.txt")
    open(txt_file, "w").close()


# GUI elements
root = tk.Tk()
root.title("SPEECH TO TEXT")
MainFrame = tk.Frame(root, bd=50, width=500, height=500)
MainFrame.pack()
lblTitle = tk.Label(MainFrame, font=('arial', 50, 'bold'), text="SPEECH TO TEXT", width=20)
lblTitle.pack()
txtSpeech = tk.Text(MainFrame, font=('arial', 30, 'italic'), width=68, height=12)
txtSpeech.pack()

btnStart = tk.Button(MainFrame, text="Start", command=start_recording)
btnStart.pack(pady=10)

btnStop = tk.Button(MainFrame, text="Stop", command=stop_recording)
btnStop.pack(pady=10)

btnConvert = tk.Button(MainFrame, text="Convert", command=convert_audio_to_text)
btnConvert.pack(pady=10)

btnReset = tk.Button(MainFrame, text="Reset", command=reset)
btnReset.pack(pady=10)

root.mainloop()
