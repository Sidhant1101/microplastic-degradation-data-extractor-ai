# Microplastic AI Extractor

Streamlit app for extracting structured experimental data from microplastic research papers.

## Setup
```powershell
cd microplastic_ai_extractor_complete
python -m pip install -r requirements.txt
```

## Groq
Add your Groq API key to `.env`:
```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Run the app and choose an available Groq model in the model field:
```powershell
python -m streamlit run app/streamlit_app.py
```

## Pipeline
PDF → AI extraction → structured experiments → normalization → validation → CSV/JSON

The app reads each PDF's text layer with PyMuPDF and sends that text to Groq; scanned pages and complex figures/tables may need a later vision/table-extraction stage.
