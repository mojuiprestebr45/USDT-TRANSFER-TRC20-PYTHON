from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
import time

# Set up TronGrid provider with the API key directly in the endpoint URL
api_key = "eb07eea7-296e-4bab-add8-96cba9cd5d32"  # Replace with your TronGrid API key
provider = HTTPProvider(endpoint_uri=f"https://api.trongrid.io?apiKey={api_key}")
tron = Tron(provider)

# Set private key and sender's address
private_key_hex = "#"  # Replace with your private key
private_key = PrivateKey(bytes.fromhex(private_key_hex))
from_address = private_key.public_key.to_base58check_address()

# USDT (TRC20) contract address
usdt_contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

# Get recipient address and amount
to_address = input("Enter the recipient's TRON address: ")
amount = float(input("Enter the amount of USDT to send: "))

# Convert the amount to the correct unit (USDT uses 6 decimals)
amount_in_sun = int(amount * 10**6)

try:
    # Access the USDT contract
    contract = tron.get_contract(usdt_contract_address)

    # Build and sign the transaction
    txn = (
        contract.functions.transfer(to_address, amount_in_sun)
        .with_owner(from_address)
        .build()
        .sign(private_key)
        .broadcast()
    )

    # Display transaction details
    print("Transaction sent successfully!")
    print("Transaction Hash:", txn["txid"])

    # Wait for confirmation
    print("Waiting for confirmation...")

    # Check if the transaction is confirmed (you can adjust the sleep time or loop for a better polling strategy)
    txn_id = txn["txid"]
    while True:
        txn_info = tron.trx.get_transaction_info(txn_id)
        if txn_info["ret"][0]["contractRet"] == "SUCCESS":
            print("Transaction confirmed!")
            break
        else:
            print("Transaction not yet confirmed. Retrying...")
            time.sleep(10)  # Wait for 10 seconds before checking again

    # Optionally, you can check gas fees here (this part is specific to Tron)
    # Tronscan API can be used to retrieve the transaction details if you need more data about the gas fees
    print("Gas fees and other transaction details can be checked on Tronscan using the txid: https://tronscan.org/#/transaction/" + txn_id)

except Exception as e:
    print("An error occurred:", e)
