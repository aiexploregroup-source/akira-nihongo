# 📦 Packaged builds

This folder holds ready-to-use builds of **AKIRA NIHONGO**.

| Platform | Artifact | Status | Notes |
|---|---|---|---|
| 🪟 Windows | [`windows/AkiraNihongo.exe`](windows/AkiraNihongo.exe) | ✅ Ready | Single-file, v1.2.0, no install required |
| 🤖 Android | — | 🛠️ Source-ready | Build with [`ANDROID.md`](../ANDROID.md) on a Linux host |

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

A prebuilt APK is intentionally not committed. PySide6 Android packages must be compiled
on a Linux/macOS host with `pyside6-android-deploy`, Buildozer, NDK r28c and JDK 17+.
The repository ships the complete `pysidedeploy.spec`; follow **[ANDROID.md](../ANDROID.md)**
to produce `bin/AkiraNihongo-debug.apk`.

## Version

Current packaged version: **1.2.0** — study planner removed, 16-stop journey, 15 real-life modules.
