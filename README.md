# Script to retrieve balance and metadata from the ethereum blockchain

#### This script uses an api key stored in the .env file that is correlated to etherscan to access data on account addresses.

This code is written in python and is using the pip package manager as per most python use cases. To install the necessary packages use `pip install -r requirements.txt` after pulling the project form github.

This code will need and etherscan api key which can be found here https://etherscan.io/

This script takes in one augment which is the address hash.
`python main.py <crypto_address>` where <crypto_address> is the supplied account address.

This code produces a csv correlated to the account address two csvs are provided for demonstration of the output.

### What I have included in CSV Output

1. crypto_address
2. balance
3. normal_transactions
4. internal_transactions
5. erc_20_transfer_events
6. erc_721_transfer_events
7. erc_1155_transfer_events

How these are represented is that the crypt address is the hash provided, balance is the balance in ether, and
normal transactions,internal_transactions, erc_20_transfer_events, erc_721_transfer_events, erc_1155_transfer_events are the number of transactions and transfer events.

### What I wanted to do if I had more time

1. Utilize the api to be able to take in multiple address and run asynchronously
2. Use the data in the transfer events and transactions to gather further data either by extracting interesting patterns or by feeding the information into other apis which can reveal more data.
3. Put in guards and error handling to prevent incorrect information being passed into the functions.
4. Convert to python module.
5. Include other cryptocurrencies such as Bitcoin and Monero.