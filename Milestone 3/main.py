from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

active_connections: dict[WebSocket, dict] = {}

async def broadcast(room: str, data: dict):
    """Sends a message only to users in the specified room."""
    for connection, info in active_connections.items():
        if info.get("room") == room:
            try:
                await connection.send_json(data)
            except Exception:
                pass

@app.get("/")
async def get():
    return {"status": "ChatterBox Milestone 3 Server is Online"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # --- EVENT: USER JOINS A ROOM ---
            if data.get("type") == "join":
                username = data.get("username", "Guest")
                room = data.get("room", "general")
                
                # Store user info associated with this websocket
                active_connections[websocket] = {"username": username, "room": room}
                
                # Notify only the people in that specific room
                await broadcast(room, {
                    "type": "system",
                    "message": f"{username} joined {room} 👋"
                })

            # --- EVENT: CHAT MESSAGE ---
            elif data.get("type") == "chat":
                user_info = active_connections.get(websocket)
                if user_info:
                    await broadcast(user_info["room"], {
                        "type": "chat",
                        "user": user_info["username"],
                        "message": data.get("message")
                    })

            # --- EVENT: TYPING INDICATOR ---
            elif data.get("type") == "typing":
                user_info = active_connections.get(websocket)
                if user_info:
                    await broadcast(user_info["room"], {
                        "type": "typing",
                        "user": user_info["username"]
                    })

            # --- EVENT: STOP TYPING ---
            elif data.get("type") == "stop_typing":
                user_info = active_connections.get(websocket)
                if user_info:
                    await broadcast(user_info["room"], {"type": "stop_typing"})

    except WebSocketDisconnect:
        # Clean up when a user leaves
        if websocket in active_connections:
            info = active_connections.pop(websocket)
            await broadcast(info["room"], {
                "type": "system",
                "message": f"{info['username']} left {info['room']} ❌"
            })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)