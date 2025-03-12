import random
import requests
import time
import os
import sys
import concurrent.futures
from cryptofuzz import Ethereum, Convertor
from colorthon import Colors

def titler(text_title: str):
    sys.stdout.write(f"\x1b]2;{text_title}\x07")
    sys.stdout.flush()

def clearNow():
    os.system("cls" if "win" in sys.platform.lower() else "clear")

def fetch_rate(url: str, amount: float) -> int:
    try:
        req = requests.get(url, timeout=5)
        req.raise_for_status()
        return int(amount * req.json()["rates"]["usd"])
    except (requests.RequestException, KeyError):
        return 0

def check_balance(url: str, address: str) -> float:
    try:
        req = requests.get(f"{url}/{address}", timeout=5)
        req.raise_for_status()
        return float(req.json().get("balance", 0)) / 1e8
    except (requests.RequestException, ValueError, KeyError):
        return 0.0

def download_bip39():
    url = "https://raw.githubusercontent.com/Pymmdrza/Dumper-Mnemonic/mainx/bip39.txt"
    try:
        req = requests.get(url, timeout=10)
        req.raise_for_status()
        with open("bip39.txt", "w", encoding="utf-8") as file:
            file.write(req.text)
        return req.text.split("\n")
    except requests.RequestException:
        print("Error downloading bip39.txt")
        sys.exit(1)

def main():
    clearNow()
    colors = Colors()
    words = open("bip39.txt").read().split("\n") if os.path.exists("bip39.txt") else download_bip39()
    eth, util = Ethereum(), Convertor()
    z = ff = found = usd = 0
    found_entries = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            z += 1
            mnemonic = " ".join(random.choices(words, k=random.choice([12, 24])))
            priv_key = util.mne_to_hex(mnemonic)
            eth_addr = eth.hex_addr(priv_key) if isinstance(eth, Ethereum) else None
            
            future_eth = executor.submit(check_balance, "https://ethbook.guarda.co/api/v2/address", eth_addr)
            future_bnb = executor.submit(check_balance, "https://bsc-nn.atomicwallet.io/api/v2/address", eth_addr)
            
            eth_bal = future_eth.result()
            bnb_bal = future_bnb.result()

            if eth_bal or bnb_bal:
                ff += 1
                usd += sum(executor.map(fetch_rate, [
                    "https://ethbook.guarda.co/api/v2/tickers/?currency=usd",
                    "https://bsc-nn.atomicwallet.io/api/v2/tickers/?currency=usd"
                ], [eth_bal, bnb_bal]))
                
                found_entries.append(
                    f"ETH: {eth_addr} | Balance: {eth_bal}\nBNB: {eth_addr} | Balance: {bnb_bal}\nMnemonic: {mnemonic}\nPrivate Key: {priv_key}\n"
                )
                if len(found_entries) >= 10:
                    with open("found.txt", "a") as file:
                        file.writelines(found_entries)
                    found_entries.clear()
                titler(f"Gen: {z} / Con: {ff} / USD: {usd} $")
            else:
                print(f"[{z} | Found:{ff}] ETH: {colors.CYAN}{eth_addr}{colors.RESET} [Balance: {eth_bal}]")
                print(f"[{z} | Found:{ff}] BNB: {colors.GREEN}{eth_addr}{colors.RESET} [Balance: {bnb_bal}]")
                print(f"[{z} | Found:{ff}] Mne: {colors.RED}{mnemonic[:64]}{colors.RESET}\n{'-'*66}")

if __name__ == "__main__":
    main()
