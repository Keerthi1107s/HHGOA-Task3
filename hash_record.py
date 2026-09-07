import hashlib
import json

# Read the verification record
with open("match_record.json", "r", encoding="utf-8") as file:
    record = json.load(file)

# Convert JSON to a consistent format
canonical_record = json.dumps(
    record,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False
)

# Calculate SHA-256 hash
record_hash = hashlib.sha256(
    canonical_record.encode("utf-8")
).hexdigest()

print("\n🔐 VERIFICATION HASH")
print("====================")
print(record_hash)

print("\n✅ SHA-256 hash created successfully.")

# Save hash
with open("record_hash.txt", "w", encoding="utf-8") as file:
    file.write(record_hash)

print("💾 Saved as: record_hash.txt")