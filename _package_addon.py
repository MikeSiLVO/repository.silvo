#!/usr/bin/env python3
"""
Addon Packaging Script for repository.silvo
Creates properly formatted addon zip files from source directories
"""

import sys
import zipfile
import os
from pathlib import Path
from xml.dom import minidom


def get_addon_info(addon_path):
    """
    Extract addon ID and version from addon.xml

    Args:
        addon_path: Path to addon directory

    Returns:
        tuple: (addon_id, version) or (None, None) if error
    """
    addon_xml = Path(addon_path) / "addon.xml"
    if not addon_xml.exists():
        print(f"Error: addon.xml not found in {addon_path}")
        return None, None

    try:
        with open(addon_xml, 'r', encoding='utf-8') as f:
            content = f.read()

        dom = minidom.parseString(content)
        addon_element = dom.getElementsByTagName('addon')[0]
        addon_id = addon_element.getAttribute('id')
        version = addon_element.getAttribute('version')

        return addon_id, version
    except Exception as e:
        print(f"Error parsing addon.xml: {e}")
        return None, None


def package_addon(addon_source, output_dir, channel=None):
    """
    Package an addon into a zip file

    Args:
        addon_source: Path to addon source directory
        output_dir: Directory to output the zip file
        channel: Optional channel name (pre-release, testing) to auto-place files

    Returns:
        str: Path to created zip file or None if error
    """
    addon_source = Path(addon_source).resolve()

    if not addon_source.exists():
        print(f"Error: Addon source not found: {addon_source}")
        return None

    addon_id, version = get_addon_info(addon_source)
    if not addon_id or not version:
        return None

    # Create output directory if needed
    output_path = Path(output_dir)
    if channel:
        # Create channel/addon.id/ structure
        output_path = output_path / channel / addon_id

    output_path.mkdir(parents=True, exist_ok=True)

    # Create zip filename
    zip_filename = f"{addon_id}-{version}.zip"
    zip_path = output_path / zip_filename

    print(f"\n{'='*60}")
    print(f"Packaging: {addon_id} v{version}")
    print(f"Source:    {addon_source}")
    print(f"Output:    {zip_path}")
    print(f"{'='*60}\n")

    # Files to exclude from zip
    exclude_patterns = [
        '.git', '.github', '.gitignore', '.gitattributes',
        '__pycache__', '*.pyc', '*.pyo', '*.pyd',
        '.vscode', '.idea', '*.swp', '*.swo',
        '.DS_Store', 'Thumbs.db', 'desktop.ini',
        '*.log', '*.tmp', '*.bak', '*.zip',
        '.claude'
    ]

    def should_exclude(path):
        """Check if path should be excluded"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern.startswith('*.'):
                # File extension pattern
                if path_str.endswith(pattern[1:]):
                    return True
            else:
                # Directory or file name pattern
                if pattern in path_str:
                    return True
        return False

    # Create zip file
    file_count = 0
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(addon_source):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]

                for file in files:
                    file_path = Path(root) / file

                    # Skip excluded files
                    if should_exclude(file_path):
                        continue

                    # Calculate archive name (relative to addon root)
                    arcname = addon_id / file_path.relative_to(addon_source)

                    zipf.write(file_path, arcname)
                    file_count += 1
                    print(f"  Added: {arcname}")

        print(f"\n✓ Successfully packaged {file_count} files")
        print(f"✓ Created: {zip_path}\n")

        # Copy metadata files to output directory if in channel mode
        if channel:
            metadata_files = ['addon.xml', 'icon.png', 'fanart.jpg']
            for meta_file in metadata_files:
                src = addon_source / meta_file
                if src.exists():
                    dst = output_path / meta_file
                    import shutil
                    shutil.copy2(src, dst)
                    print(f"  Copied metadata: {meta_file}")

        return str(zip_path)

    except Exception as e:
        print(f"\n✗ Error creating zip: {e}")
        if zip_path.exists():
            zip_path.unlink()
        return None


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║          SiLVO Addon Packaging Tool v1.0.0                   ║
╚══════════════════════════════════════════════════════════════╝
""")

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python _package_addon.py <addon_source_path> [channel]")
        print("")
        print("Examples:")
        print("  # Package to current directory")
        print("  python _package_addon.py /path/to/script.skin.info.service")
        print("")
        print("  # Package to pre-release channel (auto-creates structure)")
        print("  python _package_addon.py /path/to/script.skin.info.service pre-release")
        print("")
        print("  # Package to testing channel")
        print("  python _package_addon.py /path/to/script.skin.info.service.test testing")
        print("")
        print("Channels: pre-release, testing")
        sys.exit(1)

    addon_source = sys.argv[1]
    channel = sys.argv[2] if len(sys.argv) > 2 else None

    # Validate channel
    if channel and channel not in ['pre-release', 'testing']:
        print(f"Error: Invalid channel '{channel}'. Must be 'pre-release' or 'testing'")
        sys.exit(1)

    # Get script directory as base
    script_dir = Path(__file__).parent

    zip_path = package_addon(addon_source, script_dir, channel)

    if zip_path:
        print(f"{'='*60}")
        print("✓ Packaging completed successfully!")
        if channel:
            print(f"\nNext steps:")
            print(f"  1. Run: python _repo_generator.py {channel}")
            print(f"  2. Commit and push changes to GitHub")
        print(f"{'='*60}\n")
        sys.exit(0)
    else:
        print("✗ Packaging failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
