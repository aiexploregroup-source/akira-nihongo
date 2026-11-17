# 🤖 Building the Android APK

> **Status:** the repository is **source-ready** for Android. A prebuilt APK is intentionally
> not committed (binaries do not belong in Git, and APKs must be built against a pinned Qt
> toolchain). This guide produces a real, installable PySide6 APK.

---

## 1. Understand the constraints

PySide6 Android packaging is real, but it is **not a Windows-only workflow**:

| Requirement | Value / reason |
|---|---|
| Build host | **Linux or macOS only** — `pyside6-android-deploy` does not run on Windows. WSL2 Ubuntu works. |
| Host Python | 3.10 – 3.14 |
| JDK | **17 or newer** (Gradle used by python-for-android needs it) |
| Android NDK | **r28c** (`28.2.13676358`) — first NDK with 16 KB page-aligned binaries required by Android 15+ |
| Android SDK | `platform-tools`, `platforms;android-35`, `build-tools;35.0.0` |
| Qt modules | The Qt bootstrap supports a subset; this app uses only `Core`, `Gui`, `Widgets` |
| Architecture | `aarch64` for physical phones/tablets (`x86_64` for emulators) |
| First build | ~20–60 minutes and roughly 10–20 GB of disk |

`ui/speech.py` wraps text-to-speech in `try/except`, so if that module is unavailable on
Android the app still runs — only audio pronunciation is skipped. Everything else
(curriculum, decks, quizzes and progress) remains fully functional.

---

## 2. Set up a Linux build host

### On Windows: install WSL2 + Ubuntu

```powershell
wsl --install -d Ubuntu-22.04
```

Reboot when prompted, then open the Ubuntu terminal and continue below. If WSL is installed
but has no distro, `wsl --install -d Ubuntu-22.04` still works.

### On native Linux / inside Ubuntu

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip \
                   build-essential openjdk-17-jdk unzip wget curl

java -version     # must report 17.x
python3 --version # 3.10+
```

---

## 3. Clone and create an isolated environment

Keep the virtual environment **outside** the project directory so the deploy tool does not
try to bundle it.

```bash
cd ~
git clone https://github.com/your-username/akira-nihongo.git
python3 -m venv ~/akira-android-venv
source ~/akira-android-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "PySide6==6.12.0" buildozer cython
```

---

## 4. Download the Android wheels, NDK and SDK

### Option A — official helper (recommended)

```bash
cd ~
git clone https://code.qt.io/pyside/pyside-setup.git
cd pyside-setup
python tools/cross_compile_android/main.py \
  --download-only --skip-update --auto-accept-license
```

This caches the NDK, SDK and prebuilt target Python under `~/.pyside6-android-deploy`.
`pyside6-android-deploy` detects it automatically.

### Option B — manual downloads

```bash
# Android wheels (aarch64): download BOTH PySide6 and Shiboken6 wheels for
# Qt 6.12 / aarch64 from the official archive:
# https://download.qt.io/official_releases/QtForPython/

# Or, if qtpip is available in your environment:
qtpip download PySide6 --android --arch aarch64
qtpip download shiboken6 --android --arch aarch64
```

Install the SDK packages if you are managing them yourself:

```bash
sdkmanager "platform-tools" "platforms;android-35" "build-tools;35.0.0" \
           "ndk;28.2.13676358"
```

---

## 5. Configure `pysidedeploy.spec`

The repository already contains a generated spec. Set these values:

```ini
[app]
title = AkiraNihongo
project_dir = .
input_file = main.py

[qt]
modules = Core,Gui,Widgets

[android]
wheel_pyside   = /path/to/PySide6-6.12.0-cp310-abi3-android_aarch64.whl
wheel_shiboken = /path/to/shiboken6-6.12.0-cp310-abi3-android_aarch64.whl

[buildozer]
mode = debug          # debug -> .apk ; release -> .aab
arch = aarch64
ndk_path =            # leave empty when using the auto-detected cache
sdk_path =            # leave empty when using the auto-detected cache
```

Leave `wheel_pyside` / `wheel_shiboken` empty if you used **Option A** and the tool finds the
wheels in its cache automatically.

> **Do not** add `TextToSpeech` to `modules`. It is outside the supported Qt-for-Android
> module set, and the app already handles its absence gracefully.

---

## 6. Build

```bash
cd ~/akira-nihongo
pyside6-android-deploy --config-file pysidedeploy.spec
```

Keep the generated files if you want to tweak orientation or metadata:

```bash
pyside6-android-deploy --config-file pysidedeploy.spec --keep-deployment-files
# edit buildozer.spec (e.g. orientation = portrait) and rebuild
pyside6-android-deploy --config-file pysidedeploy.spec
```

The APK is written to `bin/`, commonly:

```text
bin/AkiraNihongo-debug.apk
```

---

## 7. Install and test

```bash
adb devices
adb install -r bin/AkiraNihongo-debug.apk
adb logcat | grep -i akira     # useful if something misbehaves
```

Test at minimum:

1. The logo-only intro finishes and the journey map appears.
2. Opening **Writing Foundations** shows centered, scrollable flashcards.
3. Reveal + rate advances progress and marks the journey stop complete.
4. The globe action switches Japanese ⇄ English and survives a restart.
5. The dark theme toggle and the real-life module still work.

---

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `Only Linux and macOS are supported` | You are on Windows — build inside WSL Ubuntu or a Linux VM. |
| Gradle asks for a newer JDK | Install JDK 17+ and set `JAVA_HOME` to it. |
| NDK version error | Use exactly r28c (`28.2.13676358`). |
| `abi3`/wheel mismatch | Download the aarch64 wheels matching Qt 6.12 and set both paths in the spec. |
| Build fails fetching Gradle dependencies | Check network/DNS; rerun — downloads are cached and resume. |
| App starts but has no audio | Expected: text-to-speech is optional on Android. |
| Layout feels cramped | The nav rail auto-collapses; rotate to landscape or report the device size. |

---

## 9. Release builds

`mode = release` produces an `.aab` for the Play Store. Signing requires your own keystore:

```bash
keytool -genkey -v -keystore akira.keystore -alias akira \
        -keyalg RSA -keysize 2048 -validity 10000
```

Configure the keystore in the generated `buildozer.spec` before a release build. Never commit
the keystore or passwords.
