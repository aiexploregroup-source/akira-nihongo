# 📦 Packaged builds

This folder holds ready-to-use builds of **AKIRA NIHONGO**.

| Platform | Artifact | Status | Notes |
|---|---|---|---|
| 🪟 Windows | [`windows/AkiraNihongo.exe`](windows/AkiraNihongo.exe) | ✅ Ready | Single-file, v1.2.0, no install required |
| 🤖 Android | [`AkiraNihongo-0.1-arm64-v8a-debug.apk`](https://github.com/aiexploregroup-source/akira-nihongo/releases/download/v1.2.0/AkiraNihongo-0.1-arm64-v8a-debug.apk) | ✅ Ready | ARM64 debug APK on the v1.2.0 release (~163 MB) |

## Windows

```powershell
.\packages\windows\AkiraNihongo.exe
```

- Single-file executable (~64 MB), fonts and the vector logo are embedded.
- Progress is stored locally at `%USERPROFILE%\.nihongo_sensei\progress.sqlite3`.
- SHA-256 checksum: [`windows/AkiraNihongo.exe.sha256`](windows/AkiraNihongo.exe.sha256)

Verify the download:

```powershell
Get-FileHash .\packages\windows\AkiraNihongo.exe -Algorithm SHA256
```

## Android

A real, installable ARM64 debug APK is attached to the
[**v1.2.0 release**](https://github.com/aiexploregroup-source/akira-nihongo/releases/tag/v1.2.0)
as `AkiraNihongo-0.1-arm64-v8a-debug.apk` (plus a `.sha256` checksum). It is not committed to Git
because at ~163 MB it exceeds GitHub's 100 MB per-file limit — release assets are the correct home
for a binary this size.

```powershell
# Install on a connected device via adb
adb install AkiraNihongo-0.1-arm64-v8a-debug.apk
```

- Bundles Qt 6.12, Python 3.14 and the full curriculum — fully offline.
- SHA-256: `6392f4330febaa49bb4603a00adb4bed1c3bef45236a176c57cfcdfed6f5f5b7`
- To rebuild from source on Linux/macOS, follow **[ANDROID.md](../ANDROID.md)**; the
  [Android build workflow](../.github/workflows/android.yml) automates the same toolchain on CI.

## Version

Current packaged version: **1.2.0** — study planner removed, 16-stop journey, 15 real-life modules.
