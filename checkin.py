"""Run the GLaDOS daily check-in task."""

from __future__ import annotations

import os
import sys
from typing import Any

import cloudscraper

CHECKIN_URL = "https://glados.cloud/api/user/checkin"
STATUS_URL = "https://glados.cloud/api/user/status"
BASE_URL = "https://glados.cloud"
REFERER = CHECKIN_URL
TOKEN = "glados.cloud"
TIMEOUT_SECONDS = 30
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/86.0.4240.75 Safari/537.36"
)


def get_cookie() -> str:
    """Read the GLaDOS cookie from the environment."""
    cookie = os.getenv("COOKIE", "").strip()
    if not cookie:
        raise RuntimeError("Missing required environment variable: COOKIE")
    return cookie


def build_headers(cookie: str) -> dict[str, str]:
    """Build the headers shared by the GLaDOS API requests."""
    return {
        "content-type": "application/json;charset=UTF-8",
        "cookie": cookie,
        "origin": BASE_URL,
        "referer": REFERER,
        "user-agent": USER_AGENT,
    }


def read_json(response: Any) -> dict[str, Any]:
    """Validate an HTTP response and return its JSON body."""
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected response format from GLaDOS")
    return data


def check_in() -> None:
    """Perform check-in and print the result."""
    scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
    headers = build_headers(get_cookie())

    checkin_response = scraper.post(
        CHECKIN_URL,
        headers=headers,
        json={"token": TOKEN},
        timeout=TIMEOUT_SECONDS,
    )
    status_response = scraper.get(
        STATUS_URL,
        headers=headers,
        timeout=TIMEOUT_SECONDS,
    )

    checkin_data = read_json(checkin_response)
    status_data = read_json(status_response)
    status_detail = status_data.get("data") or {}

    message = checkin_data.get("message")
    left_days = status_detail.get("leftDays") if isinstance(status_detail, dict) else None

    if message:
        print(message)
    if left_days is not None:
        print(left_days)


def start() -> None:
    """Backward-compatible entry point used by older deployments."""
    check_in()


def main_handler(event: object, context: object) -> None:
    """Tencent Cloud SCF compatible entry point."""
    del event, context
    check_in()


def main() -> int:
    try:
        check_in()
    except Exception as exc:
        print(f"Check-in failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
