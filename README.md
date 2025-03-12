This is an optimized version of Pymmdrza's Mnemonic-Dumper

Dumper Mnemonic

Dumper Mnemonic is a Python script designed to generate random mnemonic phrases, convert them into Ethereum private keys, and check their balances using various APIs. It has been optimized for performance with multithreading and batch file writing.

Features

Fast Execution: Uses multithreading (ThreadPoolExecutor) to handle API requests concurrently.

Optimized Mnemonic Generation: Uses random.sample() for unique word selection.

Automated Balance Checking: Queries Ethereum and Binance Smart Chain addresses for balances.

Efficient File Handling: Batch writes to found.txt to minimize disk I/O overhead.

Dynamic Terminal Updates: Displays generation statistics in the terminal title.

Requirements

Ensure you have the required dependencies installed:

pip install requests cryptofuzz colorthon

Usage

Clone the repository and navigate to the project directory:

git clone https://github.com/yourusername/Dumper-Mnemonic.git
cd Dumper-Mnemonic

Run the script:

python DumperMnemonic.py

How It Works

Loads or Downloads bip39.txt: If bip39.txt is not found, it will be downloaded automatically.

Generates Mnemonic Phrases: Randomly selects words from bip39.txt to create a mnemonic phrase.

Converts to Private Key: Uses cryptofuzz to convert the mnemonic to a private key.

Generates Ethereum and BNB Addresses: Computes the corresponding public addresses.

Checks Balance: Queries online APIs for the balance of the generated addresses.

Saves Found Wallets: If a non-zero balance is detected, the wallet details are saved to found.txt.

Output Example

[100 | Found:3] ETH: 0xabc123... [Balance: 0.5]
[101 | Found:3] BNB: 0xdef456... [Balance: 0.0]
[102 | Found:4] ETH: 0x789xyz... [Balance: 1.2]

Contributing

Feel free to fork this repository, submit pull requests, or report issues.

License

This project is licensed under the MIT License.

