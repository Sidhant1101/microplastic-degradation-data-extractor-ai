import json
import os
from openai import OpenAI
from src.schemas import ExtractionResult
from src.prompt import SYSTEM_PROMPT


def schema_for_model():
    # Pydantic's JSON schema is used as the strict structured-output contract.
    schema = ExtractionResult.model_json_schema()
    # OpenAI strict structured outputs require object properties to be required;
    # optionality is represented by nullable types in the schema.
    def make_strict(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "object" and "properties" in obj:
                obj["additionalProperties"] = False
                obj["required"] = list(obj["properties"].keys())
            for v in obj.values():
                make_strict(v)
        elif isinstance(obj, list):
            for v in obj:
                make_strict(v)
        return obj
    return make_strict(schema)


def extract_pdf(pdf_path: str, model: str | None = None) -> ExtractionResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Put it in .env or your environment.")
    model = model or os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    client = OpenAI(api_key=api_key)

    with open(pdf_path, "rb") as f:
        uploaded = client.files.create(file=f, purpose="user_data")

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_file", "file_id": uploaded.id},
                    {"type": "input_text", "text": "Extract all distinct microplastic degradation experiments from this paper. Return only the requested structured data."},
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "microplastic_extraction",
                "strict": True,
                "schema": schema_for_model(),
            }
        },
    )

    raw = response.output_text
    data = json.loads(raw)
    return ExtractionResult.model_validate(data)
