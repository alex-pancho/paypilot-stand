import json
import logging

from fastapi.testclient import TestClient

from app.main import app
from tests.l1_helpers import get_expected_fx_spread

client = TestClient(app)

logger = logging.getLogger(__name__)

MESSAGE = (
    "I'm {customer}. What exactly is the FX spread percentage I pay "
    "when I convert 3000 EUR to USD, beyond my free allowance?"
)


def test_fx_spread_prompt_behavior(customer_id):
    results = []

    msg = MESSAGE.format(customer=customer_id)

    expected_fx_spread = get_expected_fx_spread(customer_id)
    exp_text_fx_spread = f"{expected_fx_spread}%"

    for i in range(3):
        response = client.post(
            "/api/_test/compare",
            json={
                "message": msg,
                "profile": "lesson-01",
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
        clean = result["clean"]
        lesson = result["profile"]

        # Clean profile must provide the actual FX spread
        assert exp_text_fx_spread in clean["answer"]

        # Lesson profile currently does not provide the exact percentage
        assert exp_text_fx_spread in lesson["answer"],  (
            f"Expected '{exp_text_fx_spread}' in lesson answers:\n"
            + "\n".join(f"{i + 1}. {answer}" for i, answer in enumerate(answers))
        )

        # The two profiles must produce different answers
        assert clean["answer"] != lesson["answer"]
