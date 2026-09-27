import httpx
import difflib
import logging
from app import db
from app.engines import policy


def get_expected_fx_spread(customer_id: str) -> float:
    customer = db.one(
        "SELECT * FROM customers WHERE id = ?",
        (customer_id,),
    )

    assert customer is not None

    return policy.FX_SPREAD_PCT[customer["tier"]]

logger = logging.getLogger(__name__)
BASE_URL = "http://127.0.0.1:8000"

def get_system_prompt(token: str="") -> str:
    response = httpx.get(
        f"{BASE_URL}/api/_test/prompt",
        # headers={
        #     "Authorization": f"Bearer {token}",
        # },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return data

def prompt_diff(old_prompt: str, new_prompt: str) -> list[str]:
    return list(
        difflib.unified_diff(
            old_prompt.splitlines(),
            new_prompt.splitlines(),
            fromfile="old",
            tofile="new",
        )
    )


def chat(message: str) -> dict:
    response = httpx.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "test-prompt-behavior",
            "message": message,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def get_trace(request_id: str) -> dict:
    response = httpx.get(
        f"{BASE_URL}/api/_test/traces/{request_id}",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    prompt = get_system_prompt()
    print(prompt)