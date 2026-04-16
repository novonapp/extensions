import os
import json
import zipfile
import hashlib
import sys
from datetime import datetime, timezone

# --- CONFIGURATION ---
ORG_NAME = "novonapp"
REPO_NAME = "extensions"
BRANCH = "main"
REGISTRY_DISPLAY_NAME = "Novon Official Extensions"
# ---------------------

# ANSI Color Codes
CLR_G = "\033[92m" # Green
CLR_Y = "\033[93m" # Yellow
CLR_C = "\033[96m" # Cyan
CLR_R = "\033[91m" # Red
CLR_B = "\033[1m"  # Bold
CLR_0 = "\033[0m"  # Reset

BASE_URL = f"https://raw.githubusercontent.com/{ORG_NAME}/{REPO_NAME}/{BRANCH}"

def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def increment_version(v):
    parts = v.split('.')
    if parts:
        try:
            parts[-1] = str(int(parts[-1]) + 1)
        except (ValueError, IndexError):
            pass 
    return '.'.join(parts)

def bundle_extensions():
    repo_dir = "./"
    bundle_dir = os.path.join(repo_dir, "bundles")
    index_path = os.path.join(repo_dir, "index.json")
    
    # Clear screen for a clean start
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{CLR_C}{CLR_B}" + "="*60)
    print(f"  >>>  NOVON EXTENSION BUNDLER")
    print("="*60 + f"{CLR_0}")

    if not os.path.exists(repo_dir):
        print(f"{CLR_R}Error: Directory {repo_dir} not found.{CLR_0}")
        return

    upgrade_choice = input(f"\n{CLR_Y}? Do you want to automatically upgrade extension versions? (y/n): {CLR_0}").strip().lower()
    auto_upgrade = (upgrade_choice == 'y')
    
    if auto_upgrade:
        print(f"{CLR_G}[*] Auto-upgrade enabled. Incremented versions will be applied.{CLR_0}\n")
    else:
        print(f"{CLR_C}[i] Proceeding with current version numbers.{CLR_0}\n")

    if not os.path.exists(bundle_dir):
        os.makedirs(bundle_dir)
        
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    index["repoName"] = REGISTRY_DISPLAY_NAME
    index["repoUrl"] = f"{BASE_URL}/index.json"
    index["generated"] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Automatically discover all extension directories (com.novon.*)
    extensions = [d for d in os.listdir(repo_dir) 
                 if os.path.isdir(os.path.join(repo_dir, d)) and d.startswith("com.novon.")]

    for ext_id in extensions:
        ext_path = os.path.join(repo_dir, ext_id)
        
        manifest_path = os.path.join(ext_path, "manifest.json")
        source_path = os.path.join(ext_path, "source.js")
        
        if not os.path.exists(manifest_path) or not os.path.exists(source_path):
            print(f"{CLR_Y}Skipping {ext_id}: Missing manifest.json or source.js{CLR_0}")
            continue
            
        script_hash = get_sha256(source_path)
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            
        # 1. Update Version if requested
        old_version = manifest.get("version", "1.0.0")
        if auto_upgrade:
            new_version = increment_version(old_version)
            manifest["version"] = new_version
            print(f"{CLR_G}[^] Upgraded {ext_id}: {old_version} -> {new_version}{CLR_0}")
        
        # 2. Update Manifest SHA (source.js integrity)
        manifest["sha256"] = script_hash
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            
        version = manifest["version"]
        bundle_filename = f"{ext_id}-{version}.novext"
        bundle_path = os.path.join(bundle_dir, bundle_filename)
        
        # 3. Create Zip (stored as .novext)
        print(f"{CLR_C}[#] Bundling {ext_id} v{version}...{CLR_0}")
        with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(ext_path):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_full_path, ext_path)
                    zipf.write(file_full_path, arcname)
                    
        # 4. Compute Bundle Hash
        bundle_hash = get_sha256(bundle_path)
        
        # 5. Update Index
        updated = False
        for entry in index["extensions"]:
            if entry["id"] == ext_id:
                entry["version"] = version
                entry["sha256"] = bundle_hash
                entry["downloadUrl"] = f"{BASE_URL}/bundles/{bundle_filename}"
                entry["icon"] = f"{BASE_URL}/{ext_id}/icon.png"
                entry["updatedAt"] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                updated = True
                break
        
        if not updated:
            print(f"  {CLR_Y}[+] Adding {ext_id} to the index...{CLR_0}")
            entry_icon = f"{BASE_URL}/{ext_id}/icon.png"
            index["extensions"].append({
                "id": ext_id,
                "name": manifest.get("name", ext_id),
                "version": version,
                "apiVersion": manifest.get("apiVersion", "1"),
                "minAppVersion": manifest.get("minAppVersion", "0.0.1"),
                "lang": manifest.get("lang", "en"),
                "nsfw": manifest.get("nsfw", False),
                "hasCloudflare": manifest.get("hasCloudflare", False),
                "categories": manifest.get("categories", []),
                "icon": entry_icon,
                "downloadUrl": f"{BASE_URL}/bundles/{bundle_filename}",
                "sha256": bundle_hash,
                "updatedAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            })

    # 6. Write back Index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n{CLR_G}{CLR_B}[OK] Success: index.json updated with new versioning and hashes.{CLR_0}")

if __name__ == "__main__":
    bundle_extensions()
