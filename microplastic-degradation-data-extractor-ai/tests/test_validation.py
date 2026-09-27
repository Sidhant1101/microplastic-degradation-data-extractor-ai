from src.validation import validate_result

def test_bad_percentage():
    result = {"experiments": [{"endpoints": [{"endpoint_type": "mass_loss", "value": 120}]}]}
    errors, warnings = validate_result(result)
    assert errors
