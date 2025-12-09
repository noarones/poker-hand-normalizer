from pathlib import Path
from .base_parser import BaseParser

class PokerStarsParser(BaseParser):
    def __init__(self, processor):
        super().__init__(processor)

    def process_folder(self, input_dir: str = "../dataset", output_dir: str = "output"):
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        self.parse_folder(input_path, output_path)
