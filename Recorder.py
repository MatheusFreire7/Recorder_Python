import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import cv2
import pyaudio
import wave
import keyboard
import pyautogui
import numpy as np
import threading
from moviepy.editor import VideoFileClip, AudioFileClip
import pygetwindow
import time
import os

def create_round_button_with_icon(color, icon_path):
    size = 60
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((5, 5, size - 5, size - 5), fill="white")

    icon = Image.open(icon_path)
    icon = icon.convert("RGBA")
    icon = icon.resize((40, 40))
    image.paste(icon, (10, 10), icon)

    return ImageTk.PhotoImage(image)

class ScreenAudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravador de Tela e Áudio")

        self.recording = False
        self.screen_recording_started = False
        self.fps = 30
        self.tamanho_tela = tuple(pyautogui.size())
        self.codec = cv2.VideoWriter_fourcc(*"mp4v")
        self.audio = None
        
        self.audio_rate = 44100
        self.audio_format = pyaudio.paInt16
        self.recording_flag = threading.Event()  # Evento para controlar a gravação

        self.create_styles()
        self.create_interface()

    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure("TButton", padding=0, relief="flat", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 14))

    def create_interface(self):
        self.label = ttk.Label(self.root, text="Gravador de Tela e Áudio", style="TLabel")
        self.label.pack(pady=10)

        self.start_image = create_round_button_with_icon("green", "play_icon.png")
        self.start_button = ttk.Button(self.root, image=self.start_image, command=self.start_recording, style="TButton")
        self.start_button.pack(pady=10)

        self.stop_image = create_round_button_with_icon("red", "stop_icon.png")
        self.stop_button = ttk.Button(self.root, image=self.stop_image, command=self.stop_recording, state=tk.DISABLED, style="TButton")
        self.stop_button.pack(pady=10)

        self.quit_image = self.create_round_button("white")    
        self.quit_button = ttk.Button(self.root, image=self.quit_image, command=self.root.quit, style="TButton")
        self.quit_button.pack(pady=10)

        exit_image = Image.open("exit.png")  
        exit_image = exit_image.resize((40, 40))
        exit_photo = ImageTk.PhotoImage(exit_image)
        self.quit_button.config(image=exit_photo, compound="left")
        self.quit_button.image = exit_photo

        self.info_label = ttk.Label(self.root, text="Pressione ESC para parar a gravação", font=("Arial", 12, "bold"))
        self.info_label.pack()

    def create_round_button(self, color):
        size = 60
        image = Image.new("RGB", (size, size), color)
        draw = ImageDraw.Draw(image)
        draw.ellipse((5, 5, size - 5, size - 5), fill="white")
        return ImageTk.PhotoImage(image)

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        root_window = pygetwindow.getWindowsWithTitle("Gravador de Tela e Áudio")[0]
        root_window.minimize()

        def record_audio():
            audio = pyaudio.PyAudio()
            audio_stream = audio.open(
                format=self.audio_format,
                channels=1,
                rate=self.audio_rate,
                input=True,
                frames_per_buffer=1024,
            )
            frames = []

            while not self.recording_flag.is_set():
                try:
                    audio_data = audio_stream.read(1024)
                    frames.append(audio_data)
                except IOError as e:
                    print(f"Erro ao gravar áudio: {e}")

            audio_stream.stop_stream()
            audio_stream.close()
            audio.terminate()

            time.sleep(3)
            with wave.open("audio.wav", "wb") as arquivo_final:
                arquivo_final.setnchannels(1)
                arquivo_final.setsampwidth(audio.get_sample_size(self.audio_format))
                arquivo_final.setframerate(self.audio_rate)
                arquivo_final.writeframes(b"".join(frames))

        def record_screen():
            time.sleep(3)
            self.screen_recording_started = True
            out = cv2.VideoWriter("video.mp4", self.codec, self.fps, self.tamanho_tela)
            while not self.recording_flag.is_set():
                if self.screen_recording_started:
                    frame = pyautogui.screenshot()
                    frame = np.array(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    out.write(frame)

            out.release()

        def stop_recording():
            self.recording_flag.set()

        audio_thread = threading.Thread(target=record_audio)
        screen_thread = threading.Thread(target=record_screen)

        audio_thread.start()
        screen_thread.start()

        keyboard.wait("esc")
        stop_recording()

        audio_thread.join()
        screen_thread.join()
        self.stop_recording()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        root_window = pygetwindow.getWindowsWithTitle("Gravador de Tela e Áudio")[0]
        root_window.restore()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenAudioRecorderApp(root)
    root.mainloop()

    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("audio.wav")

    video_clip = video_clip.set_audio(audio_clip)

    video_clip.write_videofile("video_com_audio.mp4", codec="libx264")

     # Exclui o arquivo "video.mp4" ao encerrar o programa
    try:
         os.remove("video.mp4")
    except FileNotFoundError:
         pass