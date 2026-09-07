import subprocess
import sys
import os

print("\n" + "=" * 60)
print("🚀 HHGOA TASK #3 — FACE ID + BLOCKCHAIN VERIFICATION")
print("=" * 60)

# -------------------------------------------------
# STEP 1: Face detection + face encoding
# -------------------------------------------------
print("\n[1/4] 👤 FACE DETECTION + ENCODING")
print("-" * 40)

image_path = input("Enter image path (example: test.jpg): ").strip()

if not os.path.exists(image_path):
    print("❌ Image not found:", image_path)
    sys.exit(1)

result = subprocess.run(
    [sys.executable, "face_detect.py"],
    input=image_path + "\n",
    text=True
)

if result.returncode != 0:
    print("❌ Face detection/encoding failed.")
    sys.exit(1)

# -------------------------------------------------
# STEP 2: Reverse image search
# -------------------------------------------------
print("\n[2/4] 🔎 GOOGLE LENS REVERSE IMAGE SEARCH")
print("-" * 40)

result = subprocess.run(
    [sys.executable, "lens_search.py", image_path]
)

if result.returncode != 0:
    print("❌ Reverse image search failed.")
    sys.exit(1)

# -------------------------------------------------
# STEP 3: Create SHA-256 verification hash
# -------------------------------------------------
print("\n[3/4] 🔐 CREATING VERIFICATION HASH")
print("-" * 40)

result = subprocess.run(
    [sys.executable, "hash_record.py"]
)

if result.returncode != 0:
    print("❌ Hash creation failed.")
    sys.exit(1)

# -------------------------------------------------
# STEP 4: Record hash on Ethereum Sepolia
# -------------------------------------------------
print("\n[4/4] ⛓️ RECORDING HASH ON ETHEREUM SEPOLIA")
print("-" * 40)

result = subprocess.run(
    [sys.executable, "blockchain_record.py"]
)

if result.returncode != 0:
    print("❌ Blockchain recording failed.")
    sys.exit(1)

# -------------------------------------------------
# COMPLETE
# -------------------------------------------------
print("\n" + "=" * 60)
print("🎉 COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
print("=" * 60)

print("""
✅ Face detected
✅ Face encoding created
✅ Google Lens reverse search completed
✅ Social-media match recorded
✅ SHA-256 verification hash created
✅ Hash recorded on Ethereum Sepolia
""")

print("📁 Generated records:")
print("   • match_record.json")
print("   • record_hash.txt")
print("   • blockchain_record.json")
print("   • transaction_hash.txt")

print("\n🔥 HHGOA TASK #3 PIPELINE COMPLETE!")