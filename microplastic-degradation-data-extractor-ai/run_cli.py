import argparse
import json
import os
from dotenv import load_dotenv
from src.openai_extractor import extract_pdf
from src.normalization import normalize_result
from src.validation import validate_result

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("pdf")
parser.add_argument("--output", default="extraction.json")
parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"))
args = parser.parse_args()

result = extract_pdf(args.pdf, args.model)
data = normalize_result(result.model_dump())
errors, warnings = validate_result(data)
data["validation_errors"] = errors
data["validation_warnings"] = warnings

with open(args.output, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Saved {args.output}")
print(f"Experiments: {len(data['experiments'])}")
print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
