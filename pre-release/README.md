# Pre-Release Channel

This folder contains **beta versions** with normal addon IDs.

## Purpose

Users who install these versions will automatically upgrade to stable releases when they're published to the official Kodi repository.

## Structure

```
pre-release/
├── addons.xml                                    # Auto-generated
├── addons.xml.md5                                # Auto-generated
├── script.skin.info.service/
│   ├── addon.xml                                 # Required
│   ├── icon.png                                  # Required (512x512)
│   ├── fanart.jpg                                # Optional (1920x1080)
│   └── script.skin.info.service-2.1.0~beta.1.zip # Addon package
└── skin.aeon.nox.silvo/
    ├── addon.xml
    ├── icon.png
    ├── fanart.jpg
    └── skin.aeon.nox.silvo-1.2.0~beta.1.zip
```

## Versioning

Use tilde (~) for pre-release versions:
- `2.1.0~beta.1`
- `2.1.0~beta.2`
- `2.1.0~rc.1`

This ensures proper upgrade path: `2.1.0~beta.1 < 2.1.0~beta.2 < 2.1.0` (stable)

## Adding a New Addon

1. Create folder: `pre-release/addon.id/`
2. Copy `addon.xml`, `icon.png`, `fanart.jpg` into folder
3. Create addon zip: Use `_package_addon.py` script
4. Run `python _repo_generator.py` to update addons.xml
5. Commit and push

## Notes

- addon.xml must have correct version with ~beta suffix
- Icon must be 512x512 PNG
- Fanart should be 1920x1080 JPG (optional)
- Zip file must be named: `addon.id-version.zip`
