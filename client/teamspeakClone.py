import tkinter as tk
import tkinter.font as tkFont
import socket
import threading
import pyaudio


class App:

    def __init__(self, root):
        # setting title
        root.title("Teamspeak")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_729 = tk.Button(root)
        GButton_729["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times', size=18)
        GButton_729["font"] = ft
        GButton_729["fg"] = "#000000"
        GButton_729["justify"] = "center"
        GButton_729["text"] = "Connect"
        GButton_729.place(x=190, y=350, width=220, height=56)
        GButton_729["command"] = self.GButton_729_command

        global GMessage_676
        GMessage_676 = tk.Message(root)
        ft = tkFont.Font(family='Times', size=18)
        GMessage_676["font"] = ft
        GMessage_676["fg"] = "#333333"
        GMessage_676["justify"] = "center"
        GMessage_676["text"] = "output"
        GMessage_676.place(x=0, y=410, width=599, height=88)

        global GLineEdit_942
        GLineEdit_942 = tk.Entry(root)
        GLineEdit_942["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=18)
        GLineEdit_942["font"] = ft
        GLineEdit_942["fg"] = "#333333"
        GLineEdit_942["justify"] = "center"
        GLineEdit_942["text"] = "ServerIP"
        GLineEdit_942.place(x=190, y=120, width=214, height=59)

        global GLineEdit_17
        GLineEdit_17 = tk.Entry(root)
        GLineEdit_17["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=18)
        GLineEdit_17["font"] = ft
        GLineEdit_17["fg"] = "#333333"
        GLineEdit_17["justify"] = "center"
        GLineEdit_17["text"] = "Port"
        GLineEdit_17.place(x=190, y=220, width=213, height=54)

    def GButton_729_command(self):
        ip = GLineEdit_942.get()
        port = GLineEdit_17.get()
        connectToServer(str(ip), int(port))


def status(msg):
    GMessage_676.config(text=f"{msg}")
    GMessage_676['text'] = f"{msg}"

def connectToServer(ip, port):
    Client(ip, port)


class Client:
    def __init__(self, tIP, tPort):
        status("Ready for takeoff")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tIP = tIP
        self.tPort = tPort
        trys = 0
        while 1:
            try:
                trys += 1
                # self.target_ip = input('Enter IP address of server --> ')
                #  self.target_port = int(input('Enter target port of server --> '))
                self.s.connect((self.tIP, self.tPort))
                status(f"Trying to connect. try: {str(trys)}")
                break
            except:
                print("Couldn't connect to server")
                status("Couldn't connect to server")

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        status("Successfully connected")
        print("Connected")
        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
