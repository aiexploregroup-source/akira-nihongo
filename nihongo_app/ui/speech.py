"""Optional Japanese text-to-speech helper (gracefully degrades)."""
from __future__ import annotations

_speech = None
_available = False

try:
    from PySide6.QtTextToSpeech import QTextToSpeech

    _speech = QTextToSpeech()
    _available = bool(_speech.availableLocales())
except Exception:  # pragma: no cover - platform dependent
    _speech = None
    _available = False


def speak(text: str) -> bool:
    if not _available or _speech is None or not text:
        return False
    try:
        for locale in _speech.availableLocales():
            name = locale.name().lower().replace("_", "-")
            if name.startswith("ja"):
                _speech.setLocale(locale)
                break
        _speech.say(text)
        return True
    except Exception:
        return False


def is_available() -> bool:
    return _available
