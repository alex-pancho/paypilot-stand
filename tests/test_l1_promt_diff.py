from pathlib import Path
import logging
from tests.l1_helpers import get_system_prompt, prompt_diff
import os

os.environ.setdefault("PROFILE", "lesson-01")

PROMPTS_DIR = Path("/stand/prompts")
logger = logging.getLogger(__name__)


def load_prompt(version: str) -> str:
    return (PROMPTS_DIR / f"base.{version}.md").read_text()


def test_prompt_has_not_changed():
    old_prompt = load_prompt("v1")
    new_prompt = get_system_prompt()

    new_prompt_text = new_prompt['text']

    assert old_prompt == new_prompt_text


def test_prompt_diff_size():
    old_prompt = load_prompt("v1")
    new_prompt = get_system_prompt()

    new_prompt_text = new_prompt['text']

    old_lines = old_prompt.splitlines()
    new_lines = new_prompt_text.splitlines()

    changed_lines = sum(
        old != new
        for old, new in zip(old_lines, new_lines)
    )

    changed_lines += abs(len(old_lines) - len(new_lines))

    if changed_lines <= 2:
        diff = prompt_diff(old_prompt, new_prompt_text)
        logger.warning("\n".join(diff))
        