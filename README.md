# daily_challenge_data

JSON content repo for DailyChallenge.

## Structure

- `content/daily/daily_challenges.json`
- `content/tips/programming_tips.json`
- `content/quizzes/<topic>/multiple_choice.json`
- `content/quizzes/<topic>/multiple_select.json`
- `content/quizzes/<topic>/matching.json`
- `content/quizzes/<topic>/true_or_false.json`

Topics include `android`, `architecture`, `flutter`, `ios`, `kotlin`, and `swift`.

## Purpose

Keep learning content separate from app code and organize it by content type and topic.

## Quick Start

1. Read `content/daily/daily_challenges.json`
2. Read `content/tips/programming_tips.json`
3. Open any topic folder under `content/quizzes/`

## Validation

Run:

```bash
python3 scripts/validate_content.py
```
