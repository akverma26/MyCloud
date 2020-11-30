from channels.generic.websocket import WebsocketConsumer

from MainApp.google_api import get_drive_files_list


class WebSocket(WebsocketConsumer):
    # groups = ["broadcast"]

    def connect(self):
        # Called on connection.
        # To accept the connection call:
        self.accept()
        get_drive_files_list(self)
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        # self.accept("subprotocol")
        # To reject the connection, call:
        # self.close()
        print("Websocket connected.")

    def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        print('Data received.')
        self.send(text_data="Hello world!")
        # Or, to send a binary frame:
        # self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        # self.close()
        # Or add a custom WebSocket error code!
        # self.close(code=4123)

    def disconnect(self, close_code):
        # Called when the socket closes
        self.close()
        print("Websocket disconnected.")
