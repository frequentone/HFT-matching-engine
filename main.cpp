#include <iostream>
#include <string>
#include "OrderBook.h"

using namespace std;
using namespace TradingEngine;

int main() {
    OrderBook mybook;
    string type;
    double price, quantity;
    cout << "--- HFT TRADING TERMINAL ---" << endl;
    cout << "Commands: Buy <price> <qty> | Sell <price> <qty> | Print | Exit" << endl;
    cout << "Example: Buy 100.5 10" << endl;
    while (true) {
        cout << "\n>>";
        cin >> type;
        if (type == "Exit") {
            break;
        } else if (type == "Print") {
            mybook.printBook();
        } else if (type == "Buy" || type == "Sell") {
            cin >> price >> quantity;
            mybook.addOrder(type, price, quantity);
        } else {
            cout << "Invalid command" << endl;
        }
    }
    return 0;
}
