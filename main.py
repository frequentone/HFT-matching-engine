import os
import sys
from order_book import OrderBook

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"

def setup_console():
    if os.name == 'nt':
        os.system('color') # Enables ANSI escape processing in Windows cmd natively

def print_banner():
    banner = f"""{BOLD}{MAGENTA}
    __  ____________   ___  ___  ______    ____  _____
   / / / / ____/_  /  |__ \\/   |/ ____/   / __ \\/ ___/
  / /_/ / /_    / /   __/ / /| /___ \\    / / / /\\__ \\ 
 / __  / __/   / /   / __/ ___ |__/ /   / /_/ /___/ / 
/_/ /_/_/     /_/   /____/_/  |_/____/   \\____//____/ 
                                                        
{RESET}"""
    print(banner)
    print(f"{BOLD}{CYAN}       >> SYNAPSE: HIGH-PERFORMANCE MATCHING ENGINE <<{RESET}\n")
    print("Commands:")
    print(f"  {GREEN}Buy <price> <qty>{RESET}  - Place a buy limit order")
    print(f"  {RED}Sell <price> <qty>{RESET} - Place a sell limit order")
    print(f"  {CYAN}Print{RESET}              - View the current Limit Order Book")
    print(f"  {BOLD}Exit{RESET}               - Terminate engine\n")

def main():
    setup_console()
    print_banner()
    
    book = OrderBook()
    
    while True:
        try:
            line = input(f"{BOLD}{YELLOW}HFT_TERM>{RESET} ").strip().split()
            if not line:
                continue
                
            cmd = line[0].lower()
            if cmd == "exit":
                print(f"{MAGENTA}Terminating Matching Engine. Goodbye...{RESET}")
                break
            elif cmd == "print":
                book.print_book()
            elif cmd in ("buy", "sell"):
                if len(line) < 3:
                    print(f"{RED}[ERROR]{RESET} Invalid input. Expected: <price> <quantity>")
                    continue
                try:
                    price = float(line[1])
                    qty = float(line[2])
                    book.add_order(cmd, price, qty)
                except ValueError:
                    print(f"{RED}[ERROR]{RESET} Format error. Price and quantity must be numbers.")
            else:
                print(f"{RED}[ERROR]{RESET} Invalid command. Type 'Buy', 'Sell', 'Print', or 'Exit'.")
                
        except (KeyboardInterrupt, EOFError):
            print(f"\n{MAGENTA}Terminating Matching Engine. Goodbye...{RESET}")
            break

if __name__ == "__main__":
    main()
