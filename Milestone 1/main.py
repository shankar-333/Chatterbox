from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Chatterbox Milestone 1 - WebSocket Server Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected!")
    
    message_count = 0 
    
    try:
        while True:
            message = await websocket.receive_text()
            message_count += 1
            
            print(f"Received message #{message_count}: {message}")
            
            # Sending a modified response back to the client
            await websocket.send_text(f"Message #{message_count} received! You said: {message}")
            
    except WebSocketDisconnect:
        print("Client disconnected normally.")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
