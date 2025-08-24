from fastapi import WebSocket, status

from datetime import datetime

from models import LogItem

class ConnectionManagerGame:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, position: str) -> bool:
        if position in self.active_connections:
            await websocket.accept()
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return False
        
        else:    
            await websocket.accept()
            self.active_connections[position] = websocket
            return True
        
    async def disconnect(self, position: str):
        if position in self.active_connections:
            await self.active_connections[position].close()
            del self.active_connections[position]

    async def broadcast(self, message: dict):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)
            
class ConnectionManagerLog:
    def __init__(self):
        self.active_connection = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection = websocket

    async def disconnect(self):
        self.active_connection = None

    async def log(self, log_item: LogItem):
        try:
            log_item.time = datetime.now()
            message = log_item.model_dump_json()
            if self.active_connection is not None:
                await self.active_connection.send_text(message)
        except Exception:
            print("Error sending log message")

class ConnectionManagerWebcam:
    def __init__(self):
        self.active_connection = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection = websocket

    async def disconnect(self):
        self.active_connection = None

    async def send(self):
        # Send empty message as a request to client
        if self.active_connection is not None:
            await self.active_connection.send_text("")
            