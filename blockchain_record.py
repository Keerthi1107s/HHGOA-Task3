import os
import json
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

load_dotenv()

api_key = os.getenv("ALCHEMY_API_KEY")
private_key = os.getenv("SEPOLIA_PRIVATE_KEY")

if not api_key or not private_key:
    print("❌ Missing environment variables.")
    exit()

# Connect to Ethereum Sepolia
rpc_url = f"https://eth-sepolia.g.alchemy.com/v2/{api_key}"
web3 = Web3(Web3.HTTPProvider(rpc_url))

print("🔗 Connecting to Ethereum Sepolia...")

if not web3.is_connected():
    print("❌ Could not connect to Sepolia.")
    exit()

print("✅ Connected!")
print("⛓️ Chain ID:", web3.eth.chain_id)

# Load wallet
account = Account.from_key(private_key)

print("👛 Wallet:", account.address)

# Check balance
balance = web3.eth.get_balance(account.address)
balance_eth = web3.from_wei(balance, "ether")

print("💰 Balance:", balance_eth, "Sepolia ETH")

if balance == 0:
    print("❌ Wallet has no Sepolia ETH.")
    exit()

# Read the SHA-256 verification hash
if not os.path.exists("record_hash.txt"):
    print("❌ record_hash.txt not found.")
    exit()

with open("record_hash.txt", "r", encoding="utf-8") as file:
    record_hash = file.read().strip()

print("🔐 Verification hash:", record_hash)

# Convert hash to blockchain transaction data
data = bytes.fromhex(record_hash)

# Get transaction information
nonce = web3.eth.get_transaction_count(account.address)
gas_price = web3.eth.gas_price

transaction = {
    "from": account.address,
    "to": account.address,
    "value": 0,
    "data": data,
    "gas": 30000,
    "gasPrice": gas_price,
    "nonce": nonce,
    "chainId": 11155111
}

print("\n📤 Sending verification hash to Ethereum Sepolia...")

# Sign transaction locally
signed_transaction = account.sign_transaction(transaction)

# Send transaction
tx_hash = web3.eth.send_raw_transaction(
    signed_transaction.raw_transaction
)

print("⏳ Transaction sent!")
print("Transaction hash:", tx_hash.hex())

# Wait for confirmation
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print("\n✅ TRANSACTION CONFIRMED!")
print("Block number:", receipt.blockNumber)
print("Transaction hash:", tx_hash.hex())

# Save transaction hash
with open("transaction_hash.txt", "w", encoding="utf-8") as file:
    file.write(tx_hash.hex())

# Save blockchain record
blockchain_record = {
    "network": "Ethereum Sepolia",
    "chain_id": 11155111,
    "wallet": account.address,
    "verification_hash": record_hash,
    "transaction_hash": tx_hash.hex(),
    "block_number": receipt.blockNumber
}

with open("blockchain_record.json", "w", encoding="utf-8") as file:
    json.dump(blockchain_record, file, indent=4)

print("\n💾 Saved:")
print("  - transaction_hash.txt")
print("  - blockchain_record.json")

print("\n🔎 Verify on Sepolia Etherscan:")
print(f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}")