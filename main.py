import requests
import csv
import sys
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv('BASE_URL')
api_key = os.getenv('API_KEY')


def get_request(params):
    """ DRY way of dealing with requests.get in all the functions. Takes in params and returns response from get."""
    return requests.get(base_url, params=params)


def get_transactions_and_events(address, action):
    """ DRY way of dealing with transactions and events as they were replicated multiple times across the code.
    takes in address and action and returns the length of the response result."""
    params = {
        'module': 'account',
        'action': action,
        'address': address,
        'startblock': '0',
        'endblock': '999999999',
        'apikey': api_key
    }

    return len(get_request(params).json()['result'])

    # This commented return statement adds in all the transaction and transfer event metadata. It is unreadable in a
    # csv, so I have opted for just returning the length of the transactions to equate the amount of transactions and
    # transfer events have happened for this address. The pagination can be in the multiples of 10000s so this is best
    # way I felt to record this data in the limited time frame.

    # return get_request(params).json()['result']


def get_balance(address):
    """ Gets the balance of the account provided. Takes in Address. Returns the balance in ether or None"""
    params = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest',
        'apikey': api_key
    }

    response = get_request(params)
    data = response.json()

    if data['status'] == '1':
        balance_wei = int(data['result'])
        balance_eth = balance_wei / 1e18
        return balance_eth
    else:
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <crypto_address>")
        sys.exit(1)

    crypto_address = sys.argv[1]

    balance = get_balance(crypto_address)
    # Balance
    normal_transactions = get_transactions_and_events(crypto_address, 'txlist')
    internal_transactions = get_transactions_and_events(crypto_address, 'txlistinternal')
    erc_20_transfer_events = get_transactions_and_events(crypto_address, 'tokentx')
    erc_721_transfer_events = get_transactions_and_events(crypto_address, 'tokennfttx')
    erc_1155_transfer_events = get_transactions_and_events(crypto_address, 'token1155tx')
    # Metadata
    # Calls the api endpoints

    if balance is not None:
        metadata = {
            'crypto_address': crypto_address,
            'balance': balance,
            'normal_transactions': normal_transactions,
            'internal_transactions': internal_transactions,
            'erc_20_transfer_events': erc_20_transfer_events,
            'erc_721_transfer_events': erc_721_transfer_events,
            'erc_1155_transfer_events': erc_1155_transfer_events
        }

        output_filename = f"{crypto_address}_info.csv"
        with open(output_filename, 'w', newline='') as csvfile:
            fieldnames = metadata.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow(metadata)

        print(f"Data written to {output_filename}")
    else:
        print("Failed to retrieve balance for the given address.")


if __name__ == "__main__":
    main()
