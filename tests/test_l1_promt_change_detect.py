import json
import uuid
import logging

from tests.l1_helpers import get_expected_fx_spread, wait_for_prompt_overlay

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

logger = logging.getLogger(__name__)

MESSAGE = (
    "I'm {customer}. What exactly is the FX spread percentage I pay "
    "when I convert 3000 EUR to USD, beyond my free allowance?"
)


def test_fx_spread_prompt_behavior(customer_id, lesson_01_profile):
    actual_prompt = wait_for_prompt_overlay()
    results = []
    

    msg = MESSAGE.format(customer=customer_id)

    expected_fx_spread = get_expected_fx_spread(customer_id)
    exp_text_fx_spread = f"{expected_fx_spread}%"

    for i in range(3):
        # ВАРІАНТ З ПОРІВНЯННЯМ
        # response = client.post(
        #     "/api/_test/compare",
        #     json={
        #         "message": msg,
        #         "profile": "lesson-01",
        #     },
        # )
        session_id = str(uuid.uuid4())
        logger.info("Session ID: %s", session_id)
        response = client.post(
            "/chat",
            json={
                "session_id": session_id,
                "message": msg,
            },
        )

        response.raise_for_status()
        result = response.json()
        results.append(result)

        logger.info(
            "Compare result #%s:\n%s",
            i + 1,
            json.dumps(result, indent=2, ensure_ascii=False),
        )

    # Без циклу:
    # assert all(exp_text_fx_spread in answer for answer in answers)

    for result in results:
        
        # Clean profile must provide the actual FX spread
        # ДЛЯ ПОРІВНЯЛЬНОГО ЗАПУСКУ РОЗКОМЕНТУЙТЕ два наступні рядки
        # lesson = result["profile"]
        # clean = result["clean"]
        # assert exp_text_fx_spread in clean["answer"]

        # Lesson profile currently does not provide the exact percentage
        assert exp_text_fx_spread in result["answer"],  (
            f"Expected '{exp_text_fx_spread}' in lesson answers:\n"
            + "\n".join(f"{i + 1}. {answer}" for i, answer in enumerate(results))
        )
