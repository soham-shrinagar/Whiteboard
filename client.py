import socket
import threading
import tkinter as tk

class WhiteboardClient:
    def __init__(self, host='127.0.0.1', port=5555):
        # Logic: Set up networking
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        # Logic: Set up UI
        self.root = tk.Tk()
        self.root.title("Collaborative Whiteboard")
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=400)
        self.canvas.pack()

        # Logic: Bind left-click drag to the draw function
        self.canvas.bind("<B1-Motion>", self.send_draw_event)

        # Logic: Start a thread to listen for data from other users 
        # so the UI remains responsive while waiting for network data.
        self.listen_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.listen_thread.start()

        self.root.mainloop()

    def send_draw_event(self, event):
        # Logic: Get local mouse coordinates and draw locally
        x, y = event.x, event.y
        self.canvas.create_oval(x, y, x+2, y+2, fill="black")
        
        # Logic: Send coordinates to server
        data = f"{x},{y}"
        self.client.send(data.encode())

    def receive_data(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                if data:
                    # Logic: Parse coordinates and draw them on canvas
                    x, y = map(int, data.split(','))
                    self.canvas.create_oval(x, y, x+2, y+2, fill="red")
            except:
                break

if __name__ == "__main__":
    WhiteboardClient()