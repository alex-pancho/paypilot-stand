from pathlib import Path
import logging
from app import defects
from tests.l1_helpers import get_system_prompt, prompt_diff, wait_for_prompt_overlay
import os
import time

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

PROMPTS_DIR = Path("/stand/prompts")
logger = logging.getLogger(__name__)


def load_prompt(version: str) -> str:
    return (PROMPTS_DIR / f"base.{version}.md").read_text()


def test_prompt_has_not_changed(lesson_01_profile):

    old_prompt = load_prompt("v1")
    actual_prompt = wait_for_prompt_overlay()["text"]

    assert old_prompt == actual_prompt, "The system prompt changed unexpectedly"


# def test_prompt_diff_size(lesson_01_profile):

#     old_prompt = load_prompt("v1")
#     new_prompt = wait_for_prompt_overlay()
#     actual_prompt = new_prompt["text"]

#     profile = client.get("/health").json()
#     logger.info("PROFILE: %s", profile["profile"])

#     logger.info("Prompt version: %s", new_prompt["version"])
#     logger.info("Overlays: %s", new_prompt["overlays"])

#     old_lines = old_prompt.splitlines()
#     new_lines = actual_prompt.splitlines()

#     changed_lines = sum(
#         old != new
#         for old, new in zip(old_lines, new_lines)
#     )

#     changed_lines += abs(len(old_lines) - len(new_lines))

#     if changed_lines:
#         diff = prompt_diff(old_prompt, actual_prompt)
#         logger.warning("\n".join(diff))
