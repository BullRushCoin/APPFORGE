import json
import os

# Path to your manifest file
manifest_path = "manifest.json"

# Farcaster Mini App required fields (based on current spec)
required_fields = {
    "id": str,
    "name": str,
    "description": str,
    "version": str,
    "developer": {
        "name": str,
        "url": str
    },
    "entrypoint": str,
    "permissions": list
}

def validate_manifest(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return

    print("✅ Manifest loaded successfully.\n")

    # Validate top-level fields
    for field, expected in required_fields.items():
        if field not in manifest:
            print(f"⚠️ Missing field: '{field}'")
        else:
            if isinstance(expected, dict):
                # Nested validation for 'developer'
                for subfield, sub_type in expected.items():
                    if subfield not in manifest[field]:
                        print(f"⚠️ Missing subfield '{subfield}' in '{field}'")
                    elif not isinstance(manifest[field][subfield], sub_type):
                        print(f"⚠️ '{field}.{subfield}' should be {sub_type.__name__}")
                    else:
                        print(f"✔️ '{field}.{subfield}' is valid.")
            elif not isinstance(manifest[field], expected):
                print(f"⚠️ Field '{field}' should be {expected.__name__}")
            else:
                print(f"✔️ Field '{field}' is valid.")

    # Warn about unknown fields
    known_keys = set(required_fields.keys())
    unknown_keys = set(manifest.keys()) - known_keys
    if unknown_keys:
        print("\n🔍 Unknown fields detected:")
        for key in unknown_keys:
            print(f" - {key}")

# Run the validator
validate_manifest(manifest_path)

