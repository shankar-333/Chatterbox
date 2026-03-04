from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Chatterbox Milestone 1 - WebSocket Server Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected!")
    while True:
        try:
            message = await websocket.receive_text()
            # Echoing the message back to the client
            await websocket.send_text(f"Server Echo: {message}")
        except Exception:
            break

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
