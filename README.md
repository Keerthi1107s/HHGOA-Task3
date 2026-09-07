# HHGOA Task #3 — Face ID + Blockchain Verification

A pipeline that detects and encodes a face from a photo, finds a real matching social-media post using genuine reverse-image search, and records the verification result on the Ethereum Sepolia blockchain as a tamper-evident record.

## Pipeline

Photo
→ Face Detection (YuNet)
→ Face Encoding (SFace)
→ Google Lens Reverse Image Search
→ Social Media Match
→ SHA-256 Verification Hash
→ Ethereum Sepolia

## Features

- Detects a face using OpenCV YuNet
- Generates a face encoding using OpenCV SFace
- Performs genuine reverse-image search using Google Lens
- Automatically searches visual matches for social-media posts
- Records the matched social-media URL and verification data
- Creates a SHA-256 hash of the verification record
- Stores the hash on Ethereum Sepolia
- Produces a blockchain transaction that can be independently verified

## Technologies

- Python
- OpenCV
- YuNet
- SFace
- Google Lens via SerpApi
- SHA-256
- Web3.py
- Ethereum Sepolia testnet

## How to Run

### 1. Create and activate the virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate