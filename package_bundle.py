import zipfile
import os
from pathlib import Path

def create_bundle():
    bundle_name = "podcast-mcp.mcpb"
    source_dir = Path(".")
    
    # Files/Dirs to include
    includes = [
        "src",
        "pyproject.toml",
        "README.md",
        "manifest.json",
        ".env.example",
        "logo.svg"
    ]
    
    with zipfile.ZipFile(bundle_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in includes:
            path = source_dir / item
            if path.is_file():
                zipf.write(path, arcname=item)
                print(f"Added {item}")
            elif path.is_dir():
                for root, _, files in os.walk(path):
                    for file in files:
                        if "__pycache__" in root or file.endswith(".pyc") or file.endswith(".DS_Store"):
                            continue
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(source_dir)
                        zipf.write(file_path, arcname=arcname)
                        print(f"Added {arcname}")
    
    print(f"\nSuccessfully created {bundle_name}")

if __name__ == "__main__":
    create_bundle()
