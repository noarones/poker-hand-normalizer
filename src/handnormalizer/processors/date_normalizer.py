from __future__ import annotations

import re
from datetime import datetime


ET_TIMESTAMP_PATTERN = re.compile(
    r"\[(\d{4}/\d{2}/\d{2}\s+\d{1,2}:\d{2}:\d{2})\s+ET\]"
)


def _to_us_datetime_format(dt_str: str) -> str:
    """
    Convert 'YYYY/MM/DD HH:MM:SS' to 'MM/DD/YYYY HH:MM:SS'.
    """
    dt = datetime.strptime(dt_str, "%Y/%m/%d %H:%M:%S")
    return dt.strftime("%m/%d/%Y %H:%M:%S")


def normalize_et_timestamp_to_us_format(text: str) -> str:
 

    def _replacer(match: re.Match) -> str:
        original = match.group(1)
        us_formatted = _to_us_datetime_format(original)
        return f"[{us_formatted} ET]"

    return ET_TIMESTAMP_PATTERN.sub(_replacer, text)
