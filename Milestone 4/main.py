from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

active_connections: dict[WebSocket, dict] = {}

async def broadcast(room: str, data: dict):
    """Sends a message only to users in the same room"""
    for connection, info in active_connections.items():
        if info.get("room") == room:
            try:
                await connection.send_json(data)
            except Exception:
                pass

@app.get("/")
async def home():
    return {"status": "ChatterBox- Server Online"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "join":
                username = data.get("username", "Anonymous")
                room = data.get("room", "general")

                active_connections[websocket] = {"username": username, "room": room}
                
                await broadcast(room, {
                    "type": "system",
                    "message": f"{username} has joined the {room} 👋"
                })

            elif data.get("type") == "chat":
                user_info = active_connections.get(websocket)
                if user_info:
                    await broadcast(user_info["room"], {
                        "type": "chat",
                        "username": user_info["username"],
                        "message": data.get("message")
                    })

            elif data.get("type") == "typing":
                user_info = active_connections.get(websocket)
                if user_info:
                    await broadcast(user_info["room"], {
                        "type": "typing",
                        "username": user_info["username"]
                    })

            elif data.get("type") == "stop_typing":
                user_info = active_connections.get(websocket)
                if user_info:
                    await broadcast(user_info["room"], {"type": "stop_typing"})

    except WebSocketDisconnect:
        if websocket in active_connections:
            info = active_connections.pop(websocket)
            await broadcast(info["room"], {
                "type": "system",
                "message": f"{info['username']} has left the {info['room']} ❌"
            })

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)