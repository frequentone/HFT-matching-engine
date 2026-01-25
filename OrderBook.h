#ifndef ORDERBOOK_H
#define ORDERBOOK_H

#include <map>
#include <string>
#include <iostream>
#include <functional> 

namespace TradingEngine {

class OrderBook {
private:
    std::map<double, double> asks;
    std::map<double, double, std::greater<double>> bids;

    void match_buy_order(double price, double& quantity);
    void match_sell_order(double price, double& quantity);

public:
    void printBook();
    void addOrder(std::string type, double price, double quantity);
};

} // namespace TradingEngine

#endif // ORDERBOOK_H
