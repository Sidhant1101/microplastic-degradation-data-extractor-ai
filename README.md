# 🧪 Microplastic Degradation Data Extractor AI

**AI-powered tool for extracting structured experimental data from microplastic research papers and converting PDFs into ML-ready datasets.**

> **PDF → AI Extraction → Structured Experiments → Validation → Evidence → CSV/JSON → ML-ready Dataset**

---

## 🎯 Project Overview

Scientific information about microplastic degradation is distributed across research papers, tables, figures, supplementary information, and different experimental conditions.

Manually collecting this information from hundreds of papers is:

* Time-consuming
* Repetitive
* Difficult to standardize
* Prone to transcription errors
* Difficult to reproduce

This project aims to automate the first stage of building a research dataset by extracting experimental information from scientific papers and converting it into structured records.

The long-term goal is to create a **traceable and scientifically useful dataset for machine-learning analysis of microplastic degradation and treatment**.

---

# 🔬 Research Focus

The project primarily focuses on microplastic degradation and treatment involving:

| Polymer                    | Abbreviation |
| -------------------------- | ------------ |
| Polyethylene               | PE           |
| Polypropylene              | PP           |
| Polystyrene                | PS           |
| Polyethylene terephthalate | PET          |
| Polyvinyl chloride         | PVC          |
| Polyamide / Nylon          | PA           |

The framework can also be extended to other environmental-treatment studies.

---

# 🤖 AI Providers

The project was developed and tested using multiple AI approaches.

## 1. OpenAI

**First approach tested**

OpenAI was initially used for scientific information extraction because of its structured-output capabilities and strong language understanding.

However, for processing a large number of research papers, API usage can become **expensive**, especially when large PDF contents are processed repeatedly.

Therefore, OpenAI remains supported as an optional provider rather than the primary large-scale extraction solution.

---

## 2. Ollama

**Second approach tested**

Ollama was introduced to provide a local AI extraction option.

Current model:

```text
llama3.1:8b
```

Advantages:

* Runs locally
* No OpenAI API credits required
* Useful for development
* Greater control over local processing
* No per-request API cost

However, during testing, local extraction was **slower**, particularly for larger scientific papers.

Therefore, Ollama is useful for local experimentation and testing but may not be ideal for high-volume extraction on limited hardware.

---

## 3. Grok API

**Current fast-extraction approach**

The project also supports the **Grok API from xAI** for faster cloud-based extraction.

The motivation for adding Grok was to find a practical balance between:

```text
OpenAI
↓
Strong extraction but higher API cost

Ollama
↓
Local and no API cost but slower

Grok API
↓
Fast cloud-based extraction for large-scale processing
```

The Grok API requires an API key/token and should be configured through environment variables rather than being written directly into the source code.

### Provider Comparison

| Provider | Processing | Cost Model        | Main Use                        |
| -------- | ---------- | ----------------- | ------------------------------- |
| OpenAI   | Cloud API  | API usage         | High-quality testing/comparison |
| Ollama   | Local      | No API usage cost | Local development               |
| Grok API | Cloud API  | API usage         | Faster large-scale extraction   |

> **Note:** Actual speed, cost, and extraction quality depend on the model, paper size, hardware, API limits, and configuration.

---

# 🧠 Extraction Pipeline

The overall pipeline is:

```text
                    Research Paper
                          │
                          ▼
                         PDF
                          │
                          ▼
                  PDF Text Extraction
                          │
                          ▼
               ┌─────────────────────┐
               │    AI Provider      │
               │                     │
               │  OpenAI / Ollama   │
               │      / Grok        │
               └─────────┬───────────┘
                         │
                         ▼
                Structured Experiments
                         │
                         ▼
                    Normalization
                         │
                         ▼
                     Validation
                         │
                         ▼
                Evidence / Provenance
                         │
                         ▼
                    JSON / CSV
                         │
                         ▼
                  Research Dataset
                         │
                         ▼
                    ML Pipeline
```

---

# 📊 Information Extracted

The system is designed to extract information including:

### Polymer Information

* Polymer type
* Polymer abbreviation
* Polymer form
* Particle size

### Treatment Information

* Treatment category
* Specific treatment
* Catalyst
* Reagent
* Treatment conditions

### Experimental Conditions

* Temperature
* pH
* Treatment duration
* Initial mass
* Final mass

### Experimental Results

* Degradation
* Removal
* Adsorption
* Mass change
* Other reported endpoints

### Measurement Information

* Measurement method
* Numerical value
* Unit

### Provenance

* Source PDF
* Evidence text
* Page number
* Table reference
* Figure reference

---

# ⚠️ Scientific Data Integrity

One of the most important principles of this project is:

> **Never invent missing scientific information.**

If a paper does not report a value, the system should return:

```json
null
```

rather than estimating or guessing the value.

For example:

```json
{
    "polymer": "PS",
    "temperature_c": 25,
    "pH": null,
    "duration_h": 48
}
```

Here, `pH` is `null` because the value was not confidently extracted.

This is particularly important because incorrect values can introduce bias and noise into a machine-learning dataset.

---

# 🧪 Example Structured Experiment

A structured experiment can contain:

```json
{
    "polymer": "PS",
    "polymer_form": "microparticles",
    "particle_size": "10-50 µm",
    "treatment_category": "advanced oxidation",
    "treatment_specific": "plasma treatment",
    "catalyst_reagent": null,
    "temperature_c": 25,
    "pH": null,
    "duration_h": 2,
    "initial_mass_mg": 100,
    "final_mass_mg": 82,
    "endpoints": [
        {
            "endpoint_type": "mass loss",
            "value": 18,
            "unit": "%",
            "measurement_method": "gravimetric",
            "evidence": "...",
            "page": 5
        }
    ],
    "evidence": "...",
    "page": 5,
    "table_or_figure": "Figure 3"
}
```

The actual extracted values depend entirely on what is reported in the source paper.

---

# 🏗️ Project Structure

```text
microplastic-degradation-data-extractor-ai/
│
├── app/
│   ├── __init__.py
│   └── streamlit_app.py
│
├── src/
│   ├── __init__.py
│   ├── openai_extractor.py
│   ├── schemas.py
│   ├── prompt.py
│   ├── normalization.py
│   └── validation.py
│
├── data/
│   ├── raw/
│   │   └── papers/
│   │
│   └── extracted/
│       └── json/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🔄 Extraction Workflow

## Step 1 — Upload Research Papers

The Streamlit application supports multiple PDF uploads.

```text
Paper_01.pdf
Paper_02.pdf
Paper_03.pdf
...
```

Each paper is processed individually.

---

## Step 2 — Extract PDF Text

The current Ollama implementation uses **PyMuPDF** to extract the PDF text layer.

```text
PDF
 ↓
PyMuPDF
 ↓
Page-by-page text
```

---

## Step 3 — AI Extraction

The extracted content is passed to the selected AI provider.

```text
Scientific Text
      ↓
Extraction Prompt
      ↓
AI Model
      ↓
Structured JSON
```

The extraction prompt instructs the model to:

* identify separate experiments
* preserve units
* avoid guessing
* use `null` for missing information
* preserve evidence where possible

---

## Step 4 — Schema Validation

The response is validated using **Pydantic**.

The main structure is:

```text
ExtractionResult
       ↓
   Experiment
       ↓
    Endpoint
```

This helps keep the AI output consistent.

---

## Step 5 — Normalization

Different names for the same polymer are standardized.

```text
Polyethylene               → PE
Polypropylene              → PP
Polystyrene                → PS
Polyethylene terephthalate → PET
Polyvinyl chloride         → PVC
Polyamide                  → PA
Nylon                      → PA
```

---

## Step 6 — Validation

Basic consistency checks are performed.

Examples:

```text
Is the polymer missing?
Is the treatment missing?
Is final mass greater than initial mass?
Were zero experiments extracted?
```

Warnings are displayed in the Streamlit interface.

---

# 💻 Installation

## Requirements

Recommended:

* Python 3.10+
* Git
* Streamlit
* Ollama (optional)
* Internet connection for cloud APIs

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/microplastic-degradation-data-extractor-ai.git
```

Enter the project:

```bash
cd microplastic-degradation-data-extractor-ai
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

---

# 🦙 Ollama Setup

Install Ollama:

[Official Ollama Windows Download](https://ollama.com/download/windows?utm_source=chatgpt.com)

Check installation:

```powershell
ollama --version
```

Download the model:

```powershell
ollama pull llama3.1:8b
```

Check:

```powershell
ollama list
```

Test:

```powershell
ollama run llama3.1:8b
```

---

# 🔑 API Configuration

API keys/tokens should **never be hard-coded** into the Python files.

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=your_openai_model

GROK_API_KEY=your_grok_api_key
GROK_MODEL=your_grok_model

OLLAMA_MODEL=llama3.1:8b
```

Use your actual provider credentials locally.

### Important

Do **not** upload `.env` to GitHub.

The `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
*.zip

data/raw/papers/*.pdf
data/extracted/json/*.json
```

---

# ▶️ Running the Application

From the project directory:

```powershell
python -m streamlit run app\streamlit_app.py
```

The Streamlit interface will open in your browser.

Select the desired provider:

```text
OpenAI
Ollama
Grok
```

Then choose the corresponding model and upload your research papers.

---

# 📁 Output

The application generates two primary outputs.

## JSON

```text
microplastic_extraction.json
```

Contains the detailed structured extraction, including nested endpoints and evidence.

## CSV

```text
microplastic_experiments.csv
```

Provides a simplified tabular representation suitable for further analysis.

---

# 🔎 Evidence and Provenance

Scientific data should remain traceable to its source.

The project attempts to preserve:

```text
Source PDF
     ↓
Page
     ↓
Table / Figure
     ↓
Evidence Text
     ↓
Extracted Value
```

For example:

```json
{
    "value": 18,
    "unit": "%",
    "evidence": "The mass loss after treatment was...",
    "page": 5,
    "table_or_figure": "Figure 3"
}
```

This allows extracted values to be manually checked against the original paper.

---

# 📚 Dataset Design

The intended dataset uses:

> **One record per distinct experimental condition.**

For example:

```text
PS + Treatment A
PS + Treatment B
PS + Treatment C
```

should be represented as three separate experiments.

This prevents different experimental conditions from being incorrectly combined.

---

# 🤖 Machine Learning Pipeline

The extraction system is the first stage of a larger research workflow:

```text
Research Papers
      ↓
AI Extraction
      ↓
Structured Experiments
      ↓
Evidence + Provenance
      ↓
Normalization
      ↓
Validation
      ↓
Research Dataset
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Degradation Analysis
```

Potential future prediction targets include:

* degradation percentage
* mass loss
* degradation rate
* molecular-weight reduction
* carbonyl index
* surface oxidation
* particle-size reduction
* mineralization
* treatment efficiency

---

# 🧪 Planned Improvements

## PDF Processing

* [ ] OCR for scanned papers
* [ ] Improved table extraction
* [ ] Figure extraction
* [ ] Supplementary-information processing
* [ ] Page-level provenance

## Scientific Extraction

* [ ] Molecular-weight changes
* [ ] Surface-area changes
* [ ] Carbonyl index
* [ ] Crystallinity
* [ ] Particle-size distribution
* [ ] TOC/CO₂ mineralization
* [ ] SEM data
* [ ] FTIR data
* [ ] XPS data
* [ ] GC-MS data
* [ ] GPC data

## Dataset

* [ ] Unique paper ID
* [ ] DOI
* [ ] Authors
* [ ] Publication year
* [ ] Journal
* [ ] Experimental ID
* [ ] Source page
* [ ] Source table/figure
* [ ] Evidence snippets
* [ ] Unit normalization
* [ ] Duplicate detection

## Machine Learning

* [ ] Exploratory data analysis
* [ ] Feature engineering
* [ ] Baseline models
* [ ] Cross-validation
* [ ] Model comparison
* [ ] Explainable AI
* [ ] Degradation prediction
* [ ] Treatment optimization

---

# ⚠️ Current Limitations

The current extraction pipeline primarily works with the **text layer of PDFs**.

It may therefore have difficulty with:

* scanned PDFs
* image-only pages
* complicated tables
* graphs
* chemical structures
* information available only in figures
* supplementary information
* equations
* complex multi-column layouts

Future versions will improve table, figure, OCR, and vision-based extraction.

---

# 🔬 Scientific Reliability

This project is a **research-assistance and data-curation tool**.

AI extraction should be manually checked against the original research paper before the information is used for:

* scientific publication
* statistical analysis
* machine-learning training
* scientific conclusions

The core principle is:

```text
Traceability
     +
Validation
     +
Evidence
     +
No fabricated values
```

A missing value represented by `null` is preferable to an invented value.

---

# 🔐 Data Privacy

Do not upload confidential or unpublished research papers to external AI services without appropriate authorization.

### Ollama

Processing is performed locally on the user's machine.

### Cloud APIs

When using OpenAI or Grok, paper content is sent to the corresponding API for processing according to the provider's applicable terms and policies.

Never publish API keys or tokens in the repository.

---

# 📈 Development History

The project evolved through several extraction approaches.

### Stage 1 — OpenAI

The first implementation used OpenAI for PDF information extraction.

It provided a useful starting point for structured scientific extraction, but API costs became a concern when considering processing a large literature collection.

### Stage 2 — Ollama

Ollama was then introduced to provide a local alternative.

This removed the need for API credits, but extraction speed was slower on local hardware.

### Stage 3 — Grok API

Grok API was added as a faster cloud-based extraction option.

The current architecture therefore allows different providers to be tested using the same overall extraction pipeline.

This makes it possible to later evaluate:

```text
Extraction Speed
       +
Extraction Quality
       +
Cost
       +
Scientific Accuracy
```

rather than depending on a single AI provider.

---

# ⭐ Current Project Status

**Status: Active Development**

### Completed

* [x] Streamlit interface
* [x] Multiple PDF upload
* [x] OpenAI extraction
* [x] Ollama extraction
* [x] Grok API integration
* [x] Pydantic structured schema
* [x] Polymer normalization
* [x] Basic validation
* [x] JSON export
* [x] CSV export
* [x] Evidence/provenance fields

### In Development

* [ ] Advanced table extraction
* [ ] Figure/graph extraction
* [ ] OCR
* [ ] Improved scientific validation
* [ ] Larger literature dataset
* [ ] Advanced unit normalization
* [ ] ML feature engineering
* [ ] Degradation prediction
* [ ] Treatment optimization

---

# 📌 Core Principle

> **The goal is not simply to extract more data. The goal is to build a traceable and scientifically defensible dataset that can support reliable downstream analysis and machine learning.**

---

# 👨‍🔬 Author

**Sidhant Patel**

**BS Chemical Science**
**Indian Institute of Technology Mandi**

### Research Interests

* Microplastic degradation
* Environmental chemistry
* Green chemistry
* Computational chemistry
* Machine learning for chemistry
* Scientific data extraction
* AI-assisted scientific research

---

## Project Description

> **Fast AI-powered extraction of structured experimental data from microplastic research papers using Grok, Ollama, and OpenAI, with a focus on building traceable ML-ready datasets.**
