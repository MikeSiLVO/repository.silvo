# Quick Reference Guide

Daily workflow reference for repository.silvo automation.

## Releasing a Beta Version

```bash
# 1. Make your changes to the addon
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/script.skin.info.service

# 2. Update version in addon.xml
# Change: version="2.0.0"
# To:     version="2.1.0~beta.1"

# 3. Commit and push
git commit -am "Add feature X - beta release"
git push

# ✅ Done! Automation handles the rest
```

## Creating a Testing Version (.test)

For side-by-side installation with production version:

```bash
# 1. Create a testing branch
git checkout -b test-major-feature

# 2. Edit addon.xml manually
# Change: id="script.skin.info.service"
# To:     id="script.skin.info.service.test"
# Change: version="2.0.0"
# To:     version="2.1.0~test.1"

# 3. Update Python files (if needed)
# Search for hardcoded 'script.skin.info.service' strings
# Replace with 'script.skin.info.service.test'

# 4. Commit and push
git commit -am "Create test version for major feature"
git push

# ✅ Automation deploys to testing/ channel
```

## Version Suffixes

| Suffix | Channel | Will Upgrade to Stable? | Example |
|--------|---------|------------------------|---------|
| `~beta.1` | pre-release | ✅ Yes | `2.1.0~beta.1` |
| `~rc.1` | pre-release | ✅ Yes | `2.1.0~rc.1` |
| `~alpha.1` | pre-release | ✅ Yes | `2.1.0~alpha.1` |
| `~test.1` + `.test` ID | testing | ❌ No | `2.1.0~test.1` |
| No suffix | Not deployed | N/A | `2.1.0` |

## Checking Deployment Status

### GitHub Actions

**Addon Repo:**
https://github.com/MikeSiLVO/script.skin.info.service/actions

**Repository:**
https://github.com/MikeSiLVO/repository.silvo/actions

### Verify Deployment

```bash
# Check if your addon appears in addons.xml
curl https://mikesilvo.github.io/repository.silvo/pre-release/addons.xml

# Or visit in browser:
https://mikesilvo.github.io/repository.silvo/pre-release/
```

## Updating Icons

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/repository.silvo

# Replace icon.png and fanart.jpg in repository.silvo/
cp /path/to/new-icon.png repository.silvo/icon.png
cp /path/to/new-fanart.jpg repository.silvo/fanart.jpg

# Recreate the repository zip
cd repository.silvo
python3 -c "
import zipfile
from pathlib import Path

with zipfile.ZipFile('../repository.silvo/repository.silvo-1.0.0.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in ['addon.xml', 'icon.png', 'fanart.jpg']:
        zipf.write(file, f'repository.silvo/{file}')
"

cd ..
git commit -am "Update repository icons"
git push
```

## Manual Operations (When Needed)

### Package Addon Manually

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/repository.silvo

python _package_addon.py /path/to/addon pre-release
# or
python _package_addon.py /path/to/addon.test testing
```

### Generate Repository Files Manually

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/repository.silvo

python _repo_generator.py
# or generate specific channel
python _repo_generator.py pre-release
```

## Troubleshooting

### Deployment Not Triggering

Check addon.xml version has pre-release suffix:
```xml
<!-- ❌ Won't deploy -->
<addon id="script.skin.info.service" version="2.1.0">

<!-- ✅ Will deploy -->
<addon id="script.skin.info.service" version="2.1.0~beta.1">
```

### Wrong Channel

- `~beta`, `~rc`, `~alpha` in version → pre-release channel
- `.test` in addon ID → testing channel
- Both rules must match your intention

### Users Not Receiving Updates

- Wait 24 hours (Kodi's default update check interval)
- Verify addons.xml contains your version:
  https://mikesilvo.github.io/repository.silvo/pre-release/addons.xml
- Check GitHub Pages is deployed (takes 2-3 minutes)

### Workflow Failed

1. Click on the failed workflow in GitHub Actions
2. Read the error message
3. Common issues:
   - Missing PAT secret (`REPO_SILVO_PAT`)
   - Invalid addon.xml syntax
   - Network/GitHub timeout (just re-run)

## Repository URLs

**Installation Page:**
https://mikesilvo.github.io/repository.silvo/

**Pre-Release addons.xml:**
https://mikesilvo.github.io/repository.silvo/pre-release/addons.xml

**Testing addons.xml:**
https://mikesilvo.github.io/repository.silvo/testing/addons.xml

**Repository Zip:**
https://mikesilvo.github.io/repository.silvo/repository.silvo/repository.silvo-1.0.0.zip

## Getting User Feedback

Share this link with testers:
```
https://mikesilvo.github.io/repository.silvo/
```

They can install the repository and will automatically receive beta updates.

---

**Questions?** Check the full guides:
- `AUTOMATION_SETUP.md` - Initial setup instructions
- `README.md` - Complete repository documentation
