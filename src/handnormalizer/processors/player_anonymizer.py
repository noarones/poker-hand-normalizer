from __future__ import annotations
import re
from typing import Dict, Tuple

expresion_regular = re.compile(r"Seat\s+\d+:\s+([^\(]+)\(")

HERO_NAMES = {"noarones"}  


def build_player_mapping(text: str) -> Dict[str, str]:

    names = []
    for match in expresion_regular.finditer(text):
        raw_name = match.group(1).strip()
        if raw_name not in names:
            names.append(raw_name)

    mapping = {}
    anon_counter = 1

    for original in names:
        if original.lower() in HERO_NAMES:
            mapping[original] = "Hero"
        else:
            mapping[original] = f"Player{anon_counter}"
            anon_counter += 1

    return mapping


def apply_player_mapping(text: str, mapping: Dict[str, str]) -> str:
    for original, newname in mapping.items():
        text = text.replace(original, newname)
    return text


def anonymize_players(text: str) -> Tuple[str, Dict[str, str]]:
    mapping = build_player_mapping(text)
    anonymized_text = apply_player_mapping(text, mapping)
    return anonymized_text, mapping
