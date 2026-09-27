from src.normalization import normalize_result

def test_polymer_normalization():
    result = {"experiments": [{"polymer": "polystyrene", "duration_h": 48, "endpoints": []}]}
    out = normalize_result(result)
    assert out["experiments"][0]["polymer"] == "PS"
    assert out["experiments"][0]["duration_days"] == 2
