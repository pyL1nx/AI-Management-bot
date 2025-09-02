import re
from aiogram import types

def extract_username_and_args(message: types.Message):
    parts = (message.text or "").strip().split()
    mention = None
    args = []
    for p in parts[1:]:
        if p.startswith("@"):
            mention = p
        else:
            args.append(p)
    return mention, " ".join(args).strip()

def parse_duration_minutes(text: str, default=10):
    m = re.search(r"(\d+)", text or "")
    return int(m.group(1)) if m else default
