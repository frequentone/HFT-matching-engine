#include "OrderBook.h"

using namespace std;

namespace TradingEngine {

void OrderBook::match_buy_order(double price, double& quantity) {
    while (quantity > 0 && !asks.empty()) {
        auto best_ask = asks.begin();
        double ask_price = best_ask->first;
        double ask_quantity = best_ask->second;

        if (ask_price > price) {
            break;
        }

        cout << "[TRADE] bought at " << ask_price << endl;

        if (ask_quantity > quantity) {
            best_ask->second -= quantity;
            quantity = 0;
        } else {
            quantity -= ask_quantity;
            asks.erase(best_ask);
        }
    }
}

void OrderBook::match_sell_order(double price, double& quantity) {
    while (quantity > 0 && !bids.empty()) {
        auto best_bid = bids.begin();
        double bid_price = best_bid->first;
        double bid_quantity = best_bid->second;

        if (bid_price < price) {
            break;
        }
        cout << "[TRADE] executed at " << bid_price << endl;

        if (bid_quantity > quantity) {
            best_bid->second -= quantity;
            quantity = 0;
        } else {
            quantity -= bid_quantity;
            bids.erase(best_bid);
        }
    }
}

void OrderBook::printBook() {
    cout << "\n---ORDER BOOK---" << endl;
    for (auto it = asks.rbegin(); it != asks.rend(); ++it) {
        cout << "ASK: " << it->first << "\tQty: " << it->second << endl;
    }
    cout << "------------- (Spread)" << endl;
    for (auto it = bids.begin(); it != bids.end(); ++it) {
        cout << "BID: " << it->first << "\tQty: " << it->second << endl;
    }
    cout << "------------------\n" << endl;
}

void OrderBook::addOrder(string type, double price, double quantity) {
    if (type == "Buy") {
        match_buy_order(price, quantity);
        if (quantity > 0) {
            bids[price] += quantity;
        }
    } else if (type == "Sell") {
        match_sell_order(price, quantity);
        if (quantity > 0) {
            asks[price] += quantity;
        }
    }
}

} // namespace TradingEngine
