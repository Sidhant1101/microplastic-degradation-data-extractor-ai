import json, os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from src.schemas import ExtractionResult
from src.prompt import EXTRACTION_PROMPT
ROOT=Path(__file__).resolve().parents[1]; load_dotenv(ROOT/'.env')
def extract_pdf(pdf_path,model):
    api_key=os.getenv('GROQ_API_KEY')
    if not api_key: raise ValueError('GROQ_API_KEY is not configured. Add it to .env.')
    try: import pymupdf
    except ImportError: raise ImportError('PyMuPDF is not installed. Run: python -m pip install pymupdf')
    doc=pymupdf.open(pdf_path); pages=[]
    for n,page in enumerate(doc,1):
        text=page.get_text()
        if text.strip(): pages.append(f'\n--- PAGE {n} ---\n{text}')
    doc.close(); pdf_text='\n'.join(pages)
    if not pdf_text.strip(): raise ValueError('No readable text was found in the PDF.')
    schema=json.dumps(ExtractionResult.model_json_schema(),ensure_ascii=False)
    prompt=f'''You are a scientific data extraction assistant. Extract every distinct microplastic-related experiment. Never invent information; use null when unreported; preserve values, units, evidence, page numbers and table/figure references; keep experiments separate. Return only valid JSON matching this schema:\n{schema}\n\nINSTRUCTIONS:\n{EXTRACTION_PROMPT}\n\nPAPER:\n{pdf_text}'''
    client=OpenAI(api_key=api_key,base_url='https://api.groq.com/openai/v1')
    response=client.chat.completions.create(model=model,messages=[{'role':'user','content':prompt}],response_format={'type':'json_object'})
    content=response.choices[0].message.content
    if not content: raise ValueError('Groq returned an empty response.')
    try: return ExtractionResult.model_validate(json.loads(content))
    except json.JSONDecodeError as exc: raise ValueError(f'Groq returned invalid JSON.\n\nRaw response:\n{content}') from exc