#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PACKAGES = ROOT / "registry" / "packages"
REGISTRY_INDEX = ROOT / "registry" / "index.json"

HEADER_RE = re.compile(
    r"^AIM:\s+([a-z0-9]+(?:\.[a-z0-9]+)*)#(intent|schema|flow|contract|persona|view|event|mapping)@([0-9]+\.[0-9]+)$"
)

def parse_header(path: Path):
    try:
        raw = path.read_text(encoding="utf-8")
        lines = raw.splitlines()
        first_line = lines[0].strip() if lines else ""
        m = HEADER_RE.match(first_line)
        if m:
            return m.group(1), m.group(2), m.group(3)
    except Exception:
        pass
    return None, None, None

def build_index():
    packages = []
    
    if not REGISTRY_PACKAGES.exists():
        print(f"Error: {REGISTRY_PACKAGES} does not exist.")
        return

    # Sort package directories for deterministic output
    for pkg_dir in sorted([p for p in REGISTRY_PACKAGES.iterdir() if p.is_dir()]):
        pkg_name = pkg_dir.name
        intent_file = None
        all_files = []
        image_path = None
        version = "2.2" # Default fallback
        
        # Find all .intent files
        for f in sorted(pkg_dir.rglob("*.intent")):
            rel_f = f.relative_to(ROOT)
            all_files.append(str(rel_f))
            
            # Identify the main intent file and version
            f_name, f_facet, f_version = parse_header(f)
            if f_facet == "intent" and f_name == pkg_name:
                intent_file = str(rel_f)
                version = f_version
        
        # Check for cover image
        for img_ext in ["png", "jpg", "jpeg", "svg", "webp"]:
            img_file = pkg_dir / f"cover.{img_ext}"
            if img_file.exists():
                image_path = str(img_file.relative_to(ROOT))
                break
        
        if intent_file:
            packages.append({
                "name": pkg_name,
                "version": version,
                "entry": intent_file,
                "files": all_files,
                "image": image_path
            })
        else:
            print(f"Warning: No main intent file found for package {pkg_name}")

    index_data = {
        "version": "1",
        "packages": packages
    }
    
    with open(REGISTRY_INDEX, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2)
    
    print(f"Successfully wrote {len(packages)} packages to {REGISTRY_INDEX}")

if __name__ == "__main__":
    build_index()
