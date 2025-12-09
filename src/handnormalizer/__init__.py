from .processors.currency_converter import convert_euro_to_dollar_symbol
from .processors.player_anonymizer import anonymize_players
from .processors.character_cleaner import clean_characters
from .processors.date_normalizer import normalize_et_timestamp_to_us_format
from .processors.character_cleaner import remove_zoom


def normalize_text(text: str) -> str:

    # 1) Símbolo de moneda
    text = convert_euro_to_dollar_symbol(text)

    # 2) Anonimizar jugadores
    text, _mapping = anonymize_players(text)

    # 3) Normalizar fecha ET a formato US
    text = normalize_et_timestamp_to_us_format(text)

    text = remove_zoom(text)
    
    text = clean_characters(text)

    return text
