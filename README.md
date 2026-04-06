# ⚡ Synapse HFT: Matching Engine & Web Visualizer

![Python3](https://img.shields.io/badge/Python-3-blue.svg?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18-blue.svg?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

> Synapse HFT Viewer: A lightning-fast Limit Order Book matching engine built in Python and FastAPI. Features real-time WebSocket syncing, sub-millisecond execution tracking, and a live React dashboard.

<div align="center">
  <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&q=80&w=1000" alt="Trading Board" width="70%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.5);"/>
</div>

<br/>

## 🚀 Architecture

1. **High-Performance Backend (`server.py` & `order_book.py`)**
   - **$O(N \log N)$ Price Level Management**: Uses internal sorting mechanisms to automatically keep the bid-ask spread cached.
   - **WebSocket Streams**: Uses FastAPI + uvicorn to asynchronously broadcast tick-level market data directly to clients.
   - **Latency Tracking**: Calculates match speeds in microseconds per algorithm tick.

2. **React Web GUI (`index.html`)**
   - **Zero-Dependency Render Engine**: Deployed as a pure HTML artifact that pulls React 18, Babel, and Recharts directly from robust jsDelivr CDNs. No `npm install`, zero build steps!
   - **Live Depth Charting**: Displays market depth relative-fill bars for both asks and bids.
   - **Websocket Connectivity**: Live synchronization with backend logic without polling.

## 🛠 Features

* 📊 **Limit Order Support**: Standard Buy and Sell limit orders executed over HTTP POST or CLI.
* ⚡ **Real-time Matching**: Instantaneous cross-execution when buy/sell prices overlap.
* 🖥️ **Interactive Terminal HUD**: A stunning, colorful, interactive out-of-the-box CLI for standard testing (`main.py`).
* 📈 **Latency Metrics**: Built-in visual metrics rendering backend execution speeds on a dynamic Recharts plot.

## 🔥 Quick Start

**Terminal 1 (Backend API & Websockets)**
```bash
# Install dependencies
pip install fastapi uvicorn websockets

# Start the asynchronous backend
python server.py
```

**Terminal 2 (Frontend Dashboard)**
```bash
# Serve the lightweight React web app locally on port 8080
python -m http.server 8080
```
Navigate to `http://localhost:8080/index.html` to view the live dashboard! To place orders, interact natively with the web UI elements or spin up `python main.py` for the CLI HFT trading terminal.

---

> *"In the markets, you're either the fastest, or you're the liquidity for someone who is."*
