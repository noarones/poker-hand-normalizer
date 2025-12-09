from __future__ import annotations

import re
from typing import Dict, Tuple


SEAT_NAME_PATTERN = re.compile(r"Seat\s+\d+:\s+([^\(]+)\(")


def build_player_mapping(text: str) -> Dict[str, str]:
    """
    Look at 'Seat X: name (stack)' lines and build a mapping
    original_name -> PlayerN
    """
    names = []
    for match in SEAT_NAME_PATTERN.finditer(text):
        raw_name = match.group(1).strip()
        if raw_name not in names:
            names.append(raw_name)

    mapping = {name: f"Player{idx + 1}" for idx, name in enumerate(names)}
    return mapping


def apply_player_mapping(text: str, mapping: Dict[str, str]) -> str:
    """
    Replace all occurrences of original player names with anonymized ones.
    Simple string replace is enough after we build the mapping carefully.
    """
    for original, anon in mapping.items():
        text = text.replace(original, anon)
    return text


def anonymize_players(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Main entrypoint: return anonymized text and the mapping used.
    """
    mapping = build_player_mapping(text)
    anonymized_text = apply_player_mapping(text, mapping)
    return anonymized_text, mapping
