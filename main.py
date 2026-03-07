from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

active_connections: dict[WebSocket, str] = {}

async def broadcast(data: dict):
    for connection in list(active_connections.keys()):
        try:
            await connection.send_json(data)
        except Exception:
            if connection in active_connections:
                del active_connections[connection]

@app.get("/")
async def status():
    return {"status": "ChatterBox Milestone 2 Server is Online"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections[websocket] = "Unknown"
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "join":
                username = data.get("sender", "Guest")
                active_connections[websocket] = username
                
                await broadcast(data)
                
                await broadcast({
                    "type": "count",
                    "count": len(active_connections)
                })
            
            elif data.get("type") == "chat":
                await broadcast(data)
                
    except WebSocketDisconnect:
        username = active_connections.get(websocket, "A user")
        if websocket in active_connections:
            del active_connections[websocket]
        
        await broadcast({
            "sender": "System",
            "message": f"{username} has left the chat.",
            "type": "system"
        })
        await broadcast({"type": "count", "count": len(active_connections)})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)