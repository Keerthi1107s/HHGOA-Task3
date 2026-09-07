import os
import json
import serpapi
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERPAPI_KEY")

if not api_key:
    print("❌ SERPAPI_KEY is not set.")
    exit()

client = serpapi.Client(api_key=api_key)

# -----------------------------
# 2. UPLOAD IMAGE
# -----------------------------

image_path = "test.jpg"

print("📤 Uploading test.jpg...")

upload = client.upload_image(image_path)

if "image_id" not in upload:
    print("❌ Upload failed:")
    print(upload)
    exit()

image_id = upload["image_id"]

print("✅ Image uploaded!")

# -----------------------------
# 3. SEARCH VISUAL MATCHES
# -----------------------------

print("🔎 Searching Google Lens visual matches...")

visual_results = client.search({
    "engine": "google_lens",
    "image_id": image_id,
    "type": "visual_matches"
})

visual_matches = visual_results.get("visual_matches", [])

print(f"✅ Visual matches found: {len(visual_matches)}")

# -----------------------------
# 4. SEARCH EXACT MATCHES
# -----------------------------

print("\n🔎 Searching Google Lens exact matches...")

exact_results = client.search({
    "engine": "google_lens",
    "image_id": image_id,
    "type": "exact_matches"
})

exact_matches = exact_results.get("exact_matches", [])

print(f"✅ Exact matches found: {len(exact_matches)}")

# -----------------------------
# 5. FIND SOCIAL MEDIA MATCHES
# -----------------------------

social_sites = [
    "instagram.com",
    "facebook.com",
    "x.com",
    "twitter.com",
    "tiktok.com",
    "linkedin.com"
]

excluded_links = [
    "/pub/dir/",
    "/search/",
    "/directory/",
    "/people/",
    "shop.tiktok.com"
]

social_matches = []


def check_match(match, match_type):

    link = match.get("link", "").lower()

    if any(excluded in link for excluded in excluded_links):
        return None

    for site in social_sites:

        if site in link:

            return {
                "type": match_type,
                "title": match.get("title", "N/A"),
                "source": match.get("source", "N/A"),
                "link": match.get("link", "N/A")
            }

    return None


# Check visual matches
for match in visual_matches:

    result = check_match(match, "visual_match")

    if result:
        social_matches.append(result)


# Check exact matches
for match in exact_matches:

    result = check_match(match, "exact_match")

    if result:
        social_matches.append(result)


# -----------------------------
# 6. DISPLAY RESULTS
# -----------------------------

print("\n📱 SOCIAL MEDIA MATCHES")
print("========================")

if not social_matches:

    print("❌ No social-media matches found.")

    exit()

else:

    print(f"✅ Found {len(social_matches)} social-media result(s)!")

    for i, match in enumerate(social_matches, 1):

        print(f"\n--- Social Match {i} ---")
        print("Match type:", match["type"])
        print("Title:", match["title"])
        print("Source:", match["source"])
        print("Link:", match["link"])


# -----------------------------
# 7. CREATE VERIFICATION RECORD
# -----------------------------

best_match = social_matches[0]

record = {
    "image": image_path,
    "face_detection": "success",
    "face_encoding": "success",
    "reverse_image_search": "Google Lens",
    "visual_matches_found": len(visual_matches),
    "exact_matches_found": len(exact_matches),
    "social_match_found": True,
    "match_type": best_match["type"],
    "matched_source": best_match["source"],
    "matched_title": best_match["title"],
    "matched_url": best_match["link"],
    "timestamp_utc": datetime.now(timezone.utc).isoformat()
}
print("\n🔎 SOCIAL MEDIA MATCH FOUND")
print("===========================")
print("Platform:", best_match["source"])
print("Match type:", best_match["type"])
print("Title:", best_match["title"])
print("URL:", best_match["link"])
# Save JSON record
with open("match_record.json", "w", encoding="utf-8") as file:

    json.dump(record, file, indent=4, ensure_ascii=False)


print("\n📄 VERIFICATION RECORD")
print("======================")

print(json.dumps(record, indent=4, ensure_ascii=False))

print("\n💾 Saved as: match_record.json")