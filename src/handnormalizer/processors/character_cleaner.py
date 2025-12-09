import unicodedata
import re


def strip_accents(text: str) -> str:

    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("ascii", "ignore").decode("ascii")


def clean_special_characters(text: str) -> str:
    
    text = text.replace("&", "and")
    
    return text


def remove_zoom(text: str) -> str:
    return re.sub(r"PokerStars\s+Zoom\s+Hand\s+#", "PokerStars Hand #", text)

def clean_characters(text: str) -> str:

    text = strip_accents(text)
    text = clean_special_characters(text)
    # eliminar espacios al final de línea
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    return text
