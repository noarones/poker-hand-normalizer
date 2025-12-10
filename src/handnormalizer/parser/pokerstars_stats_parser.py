import re
from pathlib import Path
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from .base_parser import BaseParser
from handnormalizer.db.models import Hand, PlayerHandStat
from handnormalizer.db.session import SessionLocal, engine
from handnormalizer.db.models import init_db

HAND_ID_PATTERN = re.compile(r"^\s*\ufeff?PokerStars(?:\s+Zoom)?\s+Hand\s+#(\d+):")
SEAT_LINE_PATTERN = re.compile(r"Seat\s+\d+:\s+([^\(]+)\(")

class PokerStarsStatsParser(BaseParser):
    def __init__(self, processor):
        super().__init__(processor)

    def extract_hand_id(self, first_line: str) -> str:
        match = HAND_ID_PATTERN.search(first_line)
        if not match:
            raise ValueError("Could not extract hand id")
        return match.group(1)

    def extract_player_names(self, text: str) -> List[str]:
        names = []
        for match in SEAT_LINE_PATTERN.finditer(text):
            name = match.group(1).strip()
            if name not in names:
                names.append(name)
        return names

    def extract_sections(self, text: str) -> Dict[str, List[str]]:
        lines = text.splitlines()
        sections = {"preflop": [], "flop": []}
        current = None
        for line in lines:
            if line.startswith("*** HOLE CARDS ***"):
                current = "preflop"
                continue
            if line.startswith("*** FLOP ***"):
                current = "flop"
                continue
            if line.startswith("*** TURN ***") or line.startswith("*** SUMMARY ***"):
                current = None
            if current in sections:
                sections[current].append(line)
        return sections

    def compute_preflop_raises(self, preflop_lines: List[str]) -> int:
        count = 0
        for line in preflop_lines:
            if " raises " in line:
                count += 1
        return count

    def compute_flop_flags(self, flop_lines: List[str], player_names: List[str]) -> Dict[str, Dict[str, bool]]:
        result: Dict[str, Dict[str, bool]] = {}
        for name in player_names:
            result[name] = {
                "bet_flop_any": False,
                "checked_flop": False,
                "folded_flop_any": False,
            }

        for line in flop_lines:
            for name in player_names:
                if line.startswith(name + ":"):
                    if " bets " in line:
                        result[name]["bet_flop_any"] = True
                    elif " checks" in line:
                        result[name]["checked_flop"] = True
                    elif " folds" in line:
                       
                        result[name]["folded_flop_any"] = True
        return result

    def extract_hero_name(self, text: str) -> Optional[str]:

        for line in text.splitlines():
            if line.startswith("Dealt to "):
                parts = line.split()
              
                if len(parts) >= 3:
                    return parts[2]

      
        if "noarones" in text:
            return "noarones"

        return None

    def build_hand_and_stats(self, raw_text: str):
        raw_lines = raw_text.splitlines()
        if not raw_lines:
            raise ValueError("Empty hand")

        hand_id = self.extract_hand_id(raw_lines[0])
        processed = self.processor(raw_text)

        player_names = self.extract_player_names(processed)
        sections = self.extract_sections(processed)

        preflop_raises = self.compute_preflop_raises(sections["preflop"])
        is_maximum_raise_2bet = preflop_raises <= 1

        flop_flags = self.compute_flop_flags(sections["flop"], player_names)

       
        hero_name = self.extract_hero_name(processed)

        hand = Hand(
            site="PokerStars",
            site_hand_id=hand_id,
            hero_name=hero_name,
            is_maximum_raise_2bet=is_maximum_raise_2bet,
        )

        stats = []
        for name in player_names:
            flags = flop_flags.get(name, {})
            stat = PlayerHandStat(
                hand=hand,
                player_name=name,
                bet_flop_any=flags.get("bet_flop_any", False),
                checked_flop=flags.get("checked_flop", False),
                folded_flop_any=flags.get("folded_flop_any", False),
            )
            stats.append(stat)

        return hand, stats

    def ingest_folder(self, input_dir: str = "../dataset"):
        input_path = Path(input_dir)
        session: Session = SessionLocal()
        try:
            for file in input_path.glob("*.txt"):
                content = self.read_file(file)
                hands = self.split_hands(content)

                for raw_hand in hands:
                    raw_lines = raw_hand.splitlines()
                    if not raw_lines:
                        continue

                    try:
                        hand_id = self.extract_hand_id(raw_lines[0])
                    except Exception:
                        continue

                    print("HAND ID:", hand_id)

                    hand, stats = self.build_hand_and_stats(raw_hand)

                    session.add(hand)
                    for stat in stats:
                        session.add(stat)

            session.commit()
        finally:
            session.close()


def init_database():
    init_db(engine)
