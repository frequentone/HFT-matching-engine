import time
from typing import Dict, List, Callable, Any

class OrderBook:
    def __init__(self, on_trade: Callable[[Dict[str, Any]], None], on_update: Callable[[float], None]):
        self.bids: Dict[float, float] = {}
        self.asks: Dict[float, float] = {}
        self.on_trade = on_trade
        self.on_update = on_update

    def get_state(self):
        # returns sorted bids and asks
        bids = [{"price": p, "quantity": self.bids[p]} for p in sorted(self.bids.keys(), reverse=True)]
        asks = [{"price": p, "quantity": self.asks[p]} for p in sorted(self.asks.keys())]
        return {"bids": bids, "asks": asks}

    def match_buy_order(self, price: float, quantity: float) -> float:
        ask_prices = sorted(self.asks.keys())
        for ask_price in ask_prices:
            if quantity <= 0: break
            if ask_price > price: break
            
            ask_quantity = self.asks[ask_price]
            matched = min(ask_quantity, quantity)
            
            self.on_trade({
                "type": "Buy Match",
                "price": ask_price,
                "quantity": matched,
                "timestamp": time.time()
            })
            
            if ask_quantity > quantity:
                self.asks[ask_price] -= quantity
                quantity = 0
            else:
                quantity -= ask_quantity
                del self.asks[ask_price]
                
        return quantity

    def match_sell_order(self, price: float, quantity: float) -> float:
        bid_prices = sorted(self.bids.keys(), reverse=True)
        for bid_price in bid_prices:
            if quantity <= 0: break
            if bid_price < price: break
            
            bid_quantity = self.bids[bid_price]
            matched = min(bid_quantity, quantity)
            
            self.on_trade({
                "type": "Sell Match",
                "price": bid_price,
                "quantity": matched,
                "timestamp": time.time()
            })
            
            if bid_quantity > quantity:
                self.bids[bid_price] -= quantity
                quantity = 0
            else:
                quantity -= bid_quantity
                del self.bids[bid_price]
                
        return quantity

    def add_order(self, type_: str, price: float, quantity: float):
        start_time = time.perf_counter_ns()
        
        type_str = type_.lower()
        if type_str in ("buy", "b"):
            remaining = self.match_buy_order(price, quantity)
            if remaining > 0:
                self.bids[price] = self.bids.get(price, 0) + remaining
        elif type_str in ("sell", "s"):
            remaining = self.match_sell_order(price, quantity)
            if remaining > 0:
                self.asks[price] = self.asks.get(price, 0) + remaining
                
        end_time = time.perf_counter_ns()
        latency_us = (end_time - start_time) / 1000.0
        
        # After any order, update state
        self.on_update(latency_us)
