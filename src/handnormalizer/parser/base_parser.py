from pathlib import Path
from typing import List
import re

HAND_ID_PATTERN = re.compile(r"^\s*\ufeff?PokerStars(?:\s+Zoom)?\s+Hand\s+#(\d+):")
class BaseParser:
    def __init__(self, processor):
        self.processor = processor

    def read_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write_file(self, path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def split_hands(self, text: str) -> List[str]:
        lines = text.splitlines()
        hands = []
        current = []

        for line in lines:
            if HAND_ID_PATTERN.search(line) and current:
                hands.append("\n".join(current))
                current = []
            current.append(line)

        if current:
            hands.append("\n".join(current))

        return hands


    def parse_folder(self, input_folder: Path, output_folder: Path):
        for file in input_folder.glob("*.txt"):
            content = self.read_file(file)
            hands = self.split_hands(content)
            processed = [self.processor(h) for h in hands]
            output = "\n\n".join(processed)
            out_path = output_folder / file.name
            self.write_file(out_path, output)
