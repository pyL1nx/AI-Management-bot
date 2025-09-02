import json
import httpx
from ..config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL

SYSTEM_PROMPT = (
    "You are a Telegram moderation planner. "
    "Return ONLY JSON with keys: "
    "action ∈ [greet,ban,unban,mute,unmute,promote,demote,help,unknown], "
    "username (e.g., '@handle' or null), duration_minutes (int or null), reason (string or null). "
    "No extra text."
)

async def plan_action(task_text: str) -> dict:
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task_text},
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "max_tokens": 400,
        "stream": False,
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    async with httpx.AsyncClient(base_url=GROQ_BASE_URL, timeout=20) as client:
        r = await client.post("/chat/completions", json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        content = data["choices"]["message"]["content"]
    try:
        return json.loads(content)
    except Exception:
        return {"action": "unknown", "username": None, "duration_minutes": None, "reason": None}
