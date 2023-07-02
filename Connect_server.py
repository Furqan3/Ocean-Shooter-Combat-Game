import socket
import wave
import pyaudio
import time
import select


class client:
    def __init__(self,ip,port):
        self.soc= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((ip,port))
        print("connected to server")
        self.audio=None
        self.soc.setblocking(False)
    def send_text(self,text=""):
        if not text:
            return None
        self.soc.send(bytes(text,"utf-8"))
        time.sleep(1)
    def recive_text(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
        self.soc.setblocking(False)  # Set socket to non-blocking mode
        while True:
            try:
                data = self.soc.recv(1024)
            except socket.error:
                time.sleep(0.01)  # Sleep briefly if no data is available
                return None

            try:
                decoded_data = data.decode('utf-8')
                with open("textmessage.txt", "w") as file:
                    file.write(decoded_data)
            except UnicodeDecodeError:
                # play audio
                print('Playing audio')
                with open("textmessage.txt", "w") as file:
                    file.write('Audio Message')
                stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
                    
    def send_audio(self):   
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "output.wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("* recording")
        frames = []
        for _ in range(int(RATE/CHUNK*RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        with open("output.wav", "rb") as f:
            while True:
                if data := f.read(CHUNK):
                    self.sock.send(data)
                else:
                    break
        return None
