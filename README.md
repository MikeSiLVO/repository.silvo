# SiLVO Development Repository

Development and pre-release repository for **Aeon Nox: SiLVO** skin and related addons.

## 🎯 Purpose

This repository provides early access to upcoming releases for testing and feedback **before** they're submitted to the official Kodi repository.

## 📦 Installation

### Method 1: Direct Zip Install (Recommended)

1. Download: [repository.silvo-1.0.0.zip](https://mikesilvo.github.io/repository.silvo/repository.silvo/repository.silvo-1.0.0.zip)
2. In Kodi: **Settings → Add-ons → Install from zip file**
3. Select the downloaded file
4. The repository will auto-update from GitHub Pages

### Method 2: File Manager Source

1. In Kodi: **Settings → File Manager → Add source**
2. URL: `https://mikesilvo.github.io/repository.silvo/`
3. Name: `SiLVO Repo`
4. **Settings → Add-ons → Install from zip file → SiLVO Repo**
5. Install `repository.silvo-1.0.0.zip`

**Full installation guide:** https://mikesilvo.github.io/repository.silvo/

## 📢 Channels

### Pre-Release Channel

Beta versions with normal addon IDs (`script.skin.info.service`, `skin.aeon.nox.silvo`).

- Use for testing upcoming releases
- Will automatically upgrade to stable versions from official Kodi repo
- Version format: `2.0.0~beta1`, `2.0.0~beta2`

### Testing Channel

Experimental versions with modified addon IDs (`.test` suffix).

- Install side-by-side with production versions
- For testing major changes or experimental features
- Version format: `2.0.0~test1`, `2.0.0~test2`

## 🔧 Requirements

- **Kodi Version:** Omega (21.x) or newer
- **Python:** 3.0+ (built into Kodi)
- **"Unknown sources"** enabled for initial repository installation

## 🔢 Versioning

Using **tilde (~)** for pre-release versions ensures proper upgrade paths:

```
2.0.0~beta1 < 2.0.0~beta2 < 2.0.0 (stable)
```

- **Pre-release:** `2.0.0~beta1`, `2.0.0~beta2`
- **Testing:** `2.0.0~test1` (with `.test` ID suffix)
- **Stable:** `2.0.0` (official Kodi repo only)

## ⚠️ Important Notes

- This is a **testing repository** - stable releases go to official Kodi repo
- Pre-release software may contain bugs
- Testing versions (`.test` suffix) will **not** auto-upgrade to stable
- Always backup your Kodi setup before testing pre-release versions

## 📝 License

Each addon maintains its own license. Repository structure is MIT licensed.

## 📞 Support

- **Kodi Forum:** [Forum thread link]
- **GitHub Issues:** [Issues link]
- **Stable Versions:** Available in official Kodi repository

---

**Repository maintained by:** MikeSiLVO
