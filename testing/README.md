# Testing Channel

This folder contains **experimental versions** with modified addon IDs (`.test` suffix).

## Purpose

These versions can be installed **side-by-side** with production versions for comparison and testing of major changes.

## Structure

```
testing/
├── addons.xml                                         # Auto-generated
├── addons.xml.md5                                     # Auto-generated
├── script.skin.info.service.test/
│   ├── addon.xml                                      # ID must have .test suffix
│   ├── icon.png                                       # Required (512x512)
│   ├── fanart.jpg                                     # Optional (1920x1080)
│   └── script.skin.info.service.test-2.1.0~test.1.zip
└── skin.aeon.nox.silvo.test/
    ├── addon.xml
    ├── icon.png
    ├── fanart.jpg
    └── skin.aeon.nox.silvo.test-1.2.0~test.1.zip
```

## Key Differences from Pre-Release

| Aspect | Pre-Release | Testing |
|--------|-------------|---------|
| Addon ID | Normal (`script.skin.info.service`) | Modified (`.test` suffix) |
| Version | `~beta.1`, `~beta.2` | `~test.1`, `~test.2` |
| Upgrade Path | Auto-upgrades to stable | Does NOT upgrade to stable |
| Use Case | Final testing before release | Experimental feature testing |

## Creating a Testing Version

1. Copy your addon source to new folder
2. Modify `addon.xml`:
   ```xml
   <addon id="script.skin.info.service.test" version="2.1.0~test.1" ...>
   ```
3. Update all internal references:
   - Settings XML
   - Python imports if applicable
   - String IDs if needed
4. Create addon zip with `.test` suffix
5. Place in `testing/addon.id.test/`
6. Run `python _repo_generator.py`

## Important Notes

- Testing versions will **NOT** auto-upgrade to stable releases
- Users must manually uninstall testing versions
- Both production and testing versions can coexist
- Use different profile directory if addon stores data: `addon_data/addon.id.test/`

## Versioning

Use tilde (~) with test suffix:
- `2.1.0~test.1`
- `2.1.0~test.2`
- `3.0.0~test.1` (major version testing)

## When to Use Testing Channel

- Major feature rewrites
- Breaking API changes
- Performance comparison tests
- UI/UX experiments
- Database schema changes

Users can run both versions simultaneously to compare behavior.
