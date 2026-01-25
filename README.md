# High-Performance HFT Matching Engine

A low-latency **Limit Order Book (LOB)** implemented in C++ designed for high-throughput financial environments. This engine implements a **Price-Time Priority (FIFO)** matching algorithm, ensuring fair execution based on price levels and arrival sequence.

## 🚀 Performance Architecture
In high-frequency trading, every microsecond counts. This implementation focuses on minimizing "hot path" latency:

* **$O(1)$ Order Insertion**: Uses a combination of `std::unordered_map` for constant-time lookup and doubly-linked lists for fast insertion at price levels.
* **$O(1)$ Order Cancellation**: Enables immediate removal of orders via direct pointer references, bypassing the need for book-wide searches.
* **Memory Efficiency**: Optimized data structures to improve cache locality and reduce memory thrashing during high volatility.

## 🛠 Features
* **Limit Order Support**: Supports standard Buy and Sell limit orders.
* **Real-time Matching**: Instantaneous execution when buy/sell prices cross.
* **Price-Time Priority**: Adheres to the standard exchange logic where orders at the same price are prioritized by their entry time.

## 💻 Technical Stack
* **Language**: C++ (STL)
* **Patterns**: RAII (Resource Acquisition Is Initialization) for memory management and modular object-oriented design.
* **Tools**: Designed for integration with low-latency network protocols.

## 📈 Future Roadmap (The "Penthouse Plan")
* **Lock-Free Concurrency**: Implementing SPSC queues to handle asynchronous order entry.
* **SIMD Optimizations**: Utilizing AVX-512 instructions for faster price level updates.
* **FIX Protocol Integration**: Adding a gateway to support Financial Information eXchange messaging.
