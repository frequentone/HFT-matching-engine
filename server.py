import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from order_book import OrderBook

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()
trades = []

class OrderRequest(BaseModel):
    type: str # "buy" or "sell"
    price: float
    quantity: float

async def broadcast_state(latency_us=0):
    state = book.get_state()
    message = {
        "event": "state",
        "book": state,
        "latency_us": latency_us
    }
    await broadcast(message)

def sync_broadcast_state(latency_us):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(broadcast_state(latency_us))
    except RuntimeError:
        pass

async def broadcast(message: dict):
    if not clients:
        return
    text = json.dumps(message)
    dead_clients = set()
    for client in clients:
        try:
            await client.send_text(text)
        except:
            dead_clients.add(client)
    for dc in dead_clients:
        clients.remove(dc)

def on_trade(trade_event):
    trades.append(trade_event)
    if len(trades) > 50:
        trades.pop(0)
    
    message = {
        "event": "trade",
        "trade": trade_event
    }
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(broadcast(message))
    except RuntimeError:
        pass

book = OrderBook(on_trade=on_trade, on_update=sync_broadcast_state)

@app.post("/order")
async def place_order(order: OrderRequest):
    book.add_order(order.type, order.price, order.quantity)
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    
    # Send initial state and trades
    initial_message = {
        "event": "state",
        "book": book.get_state(),
        "latency_us": 0
    }
    await websocket.send_text(json.dumps(initial_message))
    
    for t in trades:
        await websocket.send_text(json.dumps({
            "event": "trade",
            "trade": t
        }))
        
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "order":
                    book.add_order(msg["type"], float(msg["price"]), float(msg["quantity"]))
            except:
                pass
    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
