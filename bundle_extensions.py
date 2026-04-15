import os
import json
import zipfile
import hashlib

def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def bundle_extensions():
    repo_dir = "./"
    bundle_dir = os.path.join(repo_dir, "bundles")
    index_path = os.path.join(repo_dir, "index.json")
    
    if not os.path.exists(bundle_dir):
        os.makedirs(bundle_dir)
        
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
        
    for ext_id in ["com.novon.kolnovel", "com.novon.mtlarabic"]:
        ext_path = os.path.join(repo_dir, ext_id)
        if not os.path.exists(ext_path):
            print(f"Skipping {ext_id}, directory not found.")
            continue
            
        # 1. Read manifest for version
        manifest_path = os.path.join(ext_path, "manifest.json")
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            
        version = manifest["version"]
        bundle_filename = f"{ext_id}-{version}.novext"
        bundle_path = os.path.join(bundle_dir, bundle_filename)
        
        # 2. Create Zip (stored as .novext)
        print(f"Bundling {ext_id} v{version} as .novext...")
        with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(ext_path):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_full_path, ext_path)
                    zipf.write(file_full_path, arcname)
                    
        # 3. Compute Hash
        file_hash = get_sha256(bundle_path)
        print(f"  SHA-256: {file_hash}")
        
        # 4. Update Index
        updated = False
        for entry in index["extensions"]:
            if entry["id"] == ext_id:
                entry["version"] = version
                entry["sha256"] = file_hash
                # Update download URL to point to the new bundle
                entry["downloadUrl"] = f"https://raw.githubusercontent.com/novol-app/test-exitension/main/bundles/{bundle_filename}"
                updated = True
                break
        
        if not updated:
            print(f"  Warning: {ext_id} not found in index.json")

    # 5. Write back Index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print("\nindex.json updated successfully.")

if __name__ == "__main__":
    bundle_extensions()
