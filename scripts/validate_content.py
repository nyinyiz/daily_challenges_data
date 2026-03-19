#!/usr/bin/env python3

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DIFFICULTIES = {"Easy", "Medium", "Hard"}
QUIZ_TOPICS = {"android", "architecture", "flutter", "ios", "kotlin", "swift"}


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}"


def validate_daily(path: Path, data: list[dict]) -> list[str]:
    errors = []
    ids = set()
    for index, item in enumerate(data, start=1):
        required = {"id", "difficulty", "question", "questionCode", "answerCode"}
        missing = required - item.keys()
        if missing:
            errors.append(f"{path}: item {index} missing fields: {sorted(missing)}")
        item_id = item.get("id")
        if item_id in ids:
            errors.append(f"{path}: duplicate id `{item_id}`")
        ids.add(item_id)
        if item.get("difficulty") not in DIFFICULTIES:
            errors.append(f"{path}: item {index} has invalid difficulty `{item.get('difficulty')}`")
    return errors


def validate_tips(path: Path, data: list[dict]) -> list[str]:
    errors = []
    ids = set()
    for index, item in enumerate(data, start=1):
        required = {"id", "category", "tip"}
        missing = required - item.keys()
        if missing:
            errors.append(f"{path}: item {index} missing fields: {sorted(missing)}")
        item_id = item.get("id")
        if item_id in ids:
            errors.append(f"{path}: duplicate id `{item_id}`")
        ids.add(item_id)
    return errors


def validate_multiple_choice(path: Path, data: list[dict]) -> list[str]:
    errors = []
    for index, item in enumerate(data, start=1):
        required = {"question", "options", "correctAnswer", "explanation", "difficulty"}
        missing = required - item.keys()
        if missing:
            errors.append(f"{path}: item {index} missing fields: {sorted(missing)}")
            continue
        if item["correctAnswer"] not in item["options"]:
            errors.append(f"{path}: item {index} correctAnswer not present in options")
        if item["difficulty"] not in DIFFICULTIES:
            errors.append(f"{path}: item {index} has invalid difficulty `{item['difficulty']}`")
    return errors


def validate_multiple_select(path: Path, data: list[dict]) -> list[str]:
    errors = []
    for index, item in enumerate(data, start=1):
        required = {"question", "options", "correctAnswers", "explanation", "difficulty"}
        missing = required - item.keys()
        if missing:
            errors.append(f"{path}: item {index} missing fields: {sorted(missing)}")
            continue
        missing_answers = [answer for answer in item["correctAnswers"] if answer not in item["options"]]
        if missing_answers:
            errors.append(f"{path}: item {index} correctAnswers missing from options: {missing_answers}")
        if item["difficulty"] not in DIFFICULTIES:
            errors.append(f"{path}: item {index} has invalid difficulty `{item['difficulty']}`")
    return errors


def validate_matching(path: Path, data: list[dict]) -> list[str]:
    errors = []
    for index, item in enumerate(data, start=1):
        required = {"question", "pairs", "explanation", "difficulty"}
        missing = required - item.keys()
        if missing:
            errors.append(f"{path}: item {index} missing fields: {sorted(missing)}")
            continue
        pairs = item["pairs"]
        if not isinstance(pairs, list) or not pairs:
            errors.append(f"{path}: item {index} has invalid pairs")
        else:
            for pair in pairs:
                if not isinstance(pair, dict) or "left" not in pair or "right" not in pair:
                    errors.append(f"{path}: item {index} contains an invalid pair entry")
                    break
        if item["difficulty"] not in DIFFICULTIES:
            errors.append(f"{path}: item {index} has invalid difficulty `{item['difficulty']}`")
    return errors


def validate_true_false(path: Path, data: list[dict]) -> list[str]:
    errors = []
    for index, item in enumerate(data, start=1):
        required = {"question", "correctAnswer", "explanation", "difficulty"}
        missing = required - item.keys()
        if missing:
            errors.append(f"{path}: item {index} missing fields: {sorted(missing)}")
            continue
        if not isinstance(item["correctAnswer"], bool):
            errors.append(f"{path}: item {index} correctAnswer must be boolean")
        if item["difficulty"] not in DIFFICULTIES:
            errors.append(f"{path}: item {index} has invalid difficulty `{item['difficulty']}`")
    return errors


def main() -> int:
    errors: list[str] = []

    expected_paths = [
        CONTENT / "daily" / "daily_challenges.json",
        CONTENT / "tips" / "programming_tips.json",
    ]

    for topic in QUIZ_TOPICS:
        base = CONTENT / "quizzes" / topic
        expected_paths.extend(
            [
                base / "multiple_choice.json",
                base / "multiple_select.json",
                base / "matching.json",
                base / "true_or_false.json",
            ]
        )

    for path in expected_paths:
        if not path.exists():
            errors.append(f"Missing expected file: {path}")

    validators = {
        "daily_challenges.json": validate_daily,
        "programming_tips.json": validate_tips,
        "multiple_choice.json": validate_multiple_choice,
        "multiple_select.json": validate_multiple_select,
        "matching.json": validate_matching,
        "true_or_false.json": validate_true_false,
    }

    for path in sorted(CONTENT.rglob("*.json")):
        data = read_json(path)
        if isinstance(data, str):
            errors.append(data)
            continue
        if not isinstance(data, list):
            errors.append(f"{path}: top-level JSON must be an array")
            continue
        validator = validators.get(path.name)
        if validator is None:
            errors.append(f"{path}: unexpected file name")
            continue
        errors.extend(validator(path, data))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
