from PT4_testing.helpers import (
    extract_ids_from_pt4_file,
    get_ids_from_parser_fold_flop,
    compare_id_lists,
)

def test_folded_flop_any():

    pt4_ids = extract_ids_from_pt4_file("folded_flop_any.txt")
    parser_ids = get_ids_from_parser_fold_flop()
    
    assert compare_id_lists(pt4_ids, parser_ids)
