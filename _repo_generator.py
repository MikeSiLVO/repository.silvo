#!/usr/bin/env python3
"""
Repository Generator for repository.silvo
Generates addons.xml and addons.xml.md5 for each channel
"""

import os
import hashlib
import sys
from pathlib import Path
from xml.dom import minidom


class RepoGenerator:
    """Generate addons.xml and addons.xml.md5 for repository channels"""

    def __init__(self, channels=None):
        """
        Initialize generator and process channels

        Args:
            channels: List of channel names to process. If None, processes all found channels.
        """
        if channels is None:
            channels = self._find_channels()

        if not channels:
            print("No channels found. Expected directories: piers")
            sys.exit(1)

        print(f"Processing {len(channels)} channel(s): {', '.join(channels)}")
        for channel in channels:
            self._generate_channel(channel)

    def _find_channels(self):
        """Find all channel directories in current path"""
        channels = []
        for item in Path('.').iterdir():
            if item.is_dir() and item.name in ['piers', 'stable', 'alpha', 'beta']:
                channels.append(item.name)
        return sorted(channels)

    def _generate_channel(self, channel):
        """
        Generate addons.xml and addons.xml.md5 for a specific channel

        Args:
            channel: Name of the channel directory
        """
        channel_path = Path(channel)
        if not channel_path.exists():
            print(f"  Warning: Channel '{channel}' does not exist, skipping")
            return

        print(f"\n{'='*60}")
        print(f"Generating for channel: {channel}/")
        print(f"{'='*60}")

        addons_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'
        addon_count = 0

        for addon_dir in sorted(channel_path.iterdir()):
            if not addon_dir.is_dir():
                continue

            addon_xml_path = addon_dir / "addon.xml"
            if not addon_xml_path.exists():
                print(f"  Skipping {addon_dir.name}/ - no addon.xml found")
                continue

            try:
                with open(addon_xml_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                dom = minidom.parseString(content)

                addon_element = dom.getElementsByTagName('addon')[0]
                addon_id = addon_element.getAttribute('id')
                addon_version = addon_element.getAttribute('version')

                for line in content.split('\n'):
                    if '<?xml' not in line:
                        addons_xml += line + '\n'

                addon_count += 1
                print(f"  ✓ Added: {addon_id} v{addon_version}")

            except Exception as e:
                print(f"  ✗ Error processing {addon_dir.name}/addon.xml: {e}")
                continue

        addons_xml += '</addons>\n'

        if addon_count == 0:
            print(f"  Warning: No valid addons found in {channel}/")
            return

        addons_xml_path = channel_path / "addons.xml"
        addons_xml_path.write_text(addons_xml, encoding='utf-8')
        print(f"\n  Generated: {addons_xml_path}")

        md5_hash = hashlib.md5(addons_xml.encode('utf-8')).hexdigest()
        md5_path = channel_path / "addons.xml.md5"
        md5_path.write_text(md5_hash, encoding='utf-8')
        print(f"  Generated: {md5_path}")
        print(f"  MD5: {md5_hash}")
        print(f"  Total addons: {addon_count}")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║          SiLVO Repository Generator v1.0.0                   ║
╚══════════════════════════════════════════════════════════════╝
""")

    channels_arg = sys.argv[1:] if len(sys.argv) > 1 else None

    try:
        RepoGenerator(channels=channels_arg)
        print(f"\n{'='*60}")
        print("✓ Repository generation completed successfully!")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
