import os
from web3 import Web3

# Get Alchemy API key
api_key = os.getenv("ALCHEMY_API_KEY")

if not api_key:
    print("❌ ALCHEMY_API_KEY is not set.")
    exit()

# Sepolia RPC
rpc_url = f"https://eth-sepolia.g.alchemy.com/v2/{api_key}"

# Connect to Sepolia
web3 = Web3(Web3.HTTPProvider(rpc_url))

print("🔗 Connecting to Ethereum Sepolia...")

if web3.is_connected():
    print("✅ Connected to Ethereum Sepolia!")
    print("⛓️ Chain ID:", web3.eth.chain_id)
    print("🔢 Latest block:", web3.eth.block_number)
else:
    print("❌ Could not connect to Sepolia.")