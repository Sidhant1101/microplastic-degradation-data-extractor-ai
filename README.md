# microplastic-degradation-data-extractor-ai
AI-powered tool for extracting structured experimental data from microplastic research papers and converting PDFs into ML-ready datasets.
# 🧪 Microplastic AI Extractor

**AI-powered extraction of structured experimental data from microplastic research papers.**

> **PDF → Scientific Information Extraction → Structured Experiments → Validation → CSV/JSON → ML-ready Dataset**

This project is being developed to build a reliable research dataset for studying **microplastic degradation and treatment** using machine learning.

The system extracts experimental information from scientific research papers and converts unstructured PDF content into structured experimental records while preserving **evidence, units, experimental conditions, and provenance**.

---

## 🎯 Project Goal

Scientific literature contains a large amount of experimental information, but this information is usually stored in:

* PDF paragraphs
* tables
* figures
* supplementary information
* different units
* inconsistent terminology
* different experimental conditions

Manually collecting this information for hundreds of papers is slow and error-prone.

The goal of this project is to create an automated pipeline that can transform:

```text
Scientific Research Paper
        ↓
       PDF
        ↓
   Text Extraction
        ↓
    AI Extraction
        ↓
Structured Experiments
        ↓
Normalization
        ↓
Validation
        ↓
Evidence / Provenance
        ↓
     CSV / JSON
        ↓
  ML-ready Dataset
```

The long-term objective is to use the resulting dataset for **machine-learning models that can analyze and predict microplastic degradation behavior**.

---

# 🔬 Target Research Area

The project focuses primarily on microplastic degradation and treatment involving polymers such as:

| Polymer                    | Abbreviation |
| -------------------------- | ------------ |
| Polyethylene               | PE           |
| Polypropylene              | PP           |
| Polystyrene                | PS           |
| Polyethylene terephthalate | PET          |
| Polyvinyl chloride         | PVC          |
| Polyamide / Nylon          | PA           |

The extraction framework can also process related environmental-treatment experiments when relevant.

---

# 🚀 Current Features

### 📄 Multiple PDF Upload

Upload multiple research papers simultaneously.

```text
Paper_01.pdf
Paper_02.pdf
Paper_03.pdf
...
```

The application processes each paper individually and combines the extracted experiments.

---

### 🤖 Multiple AI Providers

The application supports:

#### Ollama

Runs locally on your computer.

Advantages:

* No OpenAI API credits required
* Local processing
* Useful for development and experimentation
* Works offline after the model has been downloaded

Current default model:

```text
llama3.1:8b
```

#### OpenAI

The project also contains an OpenAI extraction backend.

OpenAI requires:

* an API key
* available API credits
* a compatible model

---

# 📊 Extracted Information

The extractor attempts to identify information such as:

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

### Results

* Degradation
* Removal
* Adsorption
* Mass change
* Other reported endpoints

### Measurement Information

* Measurement method
* Reported value
* Unit

### Scientific Provenance

* Evidence text
* Page number
* Table reference
* Figure reference
* Source PDF

---

# ⚠️ Scientific Data Integrity

A major design principle of this project is:

> **Do not guess missing scientific information.**

If a research paper does not report a value, the extractor should return:

```json
null
```

instead of inventing a value.

For example:

```json
{
    "polymer": "PS",
    "temperature_c": 25,
    "pH": null,
    "duration_h": 48
}
```

Here, `pH` was not reported or could not be confidently extracted.

This is important because fabricated values could introduce serious errors into the final machine-learning dataset.

---

# 🧠 Example Structured Experiment

An extracted experiment may look like:

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

The actual output depends entirely on what is reported in the paper.

---

# 🏗️ Project Architecture

```text
microplastic_ai_extractor/
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

# 🔄 Extraction Pipeline

## 1. Upload PDF

Research papers are uploaded through the Streamlit interface.

```text
PDF
 ↓
Streamlit uploader
```

---

## 2. PDF Processing

For Ollama, the current implementation uses **PyMuPDF** to extract the text layer from the PDF.

```text
PDF
 ↓
PyMuPDF
 ↓
Page-by-page text
```

Page information is retained so that extracted evidence can be associated with a page.

---

## 3. AI Extraction

The extracted text is passed to the selected AI model.

```text
Scientific text
       ↓
Extraction prompt
       ↓
AI model
       ↓
Structured JSON
```

The model is instructed to:

* extract experiments separately
* preserve units
* avoid guessing
* return `null` for missing information
* preserve evidence where possible

---

## 4. Schema Validation

The extracted response is validated using **Pydantic**.

The main objects are:

```text
ExtractionResult
       ↓
Experiment
       ↓
Endpoint
```

This helps ensure that the AI output follows the expected structure.

---

## 5. Normalization

Different ways of writing the same polymer are converted into standardized abbreviations.

For example:

```text
Polyethylene → PE
Polypropylene → PP
Polystyrene → PS
Polyethylene terephthalate → PET
Polyvinyl chloride → PVC
Polyamide → PA
Nylon → PA
```

---

## 6. Validation

Basic scientific consistency checks are performed.

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

Recommended environment:

* Windows / Linux / macOS
* Python 3.10+
* Git
* Ollama
* Streamlit

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/microplastic-ai-extractor.git
```

Move into the project:

```bash
cd microplastic-ai-extractor
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can alternatively use:

```powershell
.venv\Scripts\activate.bat
```

---

## 3. Install Python Dependencies

```powershell
python -m pip install -r requirements.txt
```

The main dependencies are:

```text
streamlit
pandas
python-dotenv
openai
pydantic
ollama
pymupdf
```

---

# 🦙 Ollama Setup

Ollama is the recommended option for development because it can run locally without OpenAI API credits.

Download Ollama:

[Ollama for Windows](https://ollama.com/download/windows?utm_source=chatgpt.com)

After installation, open a **new terminal**.

Check:

```powershell
ollama --version
```

---

## Download the Model

```powershell
ollama pull llama3.1:8b
```

Check installed models:

```powershell
ollama list
```

You should see:

```text
NAME
llama3.1:8b
```

---

## Test Ollama

```powershell
ollama run llama3.1:8b
```

Then try:

```text
What is polyethylene?
```

If the model responds, Ollama is ready.

---

# ▶️ Running the Application

From the project directory:

```powershell
python -m streamlit run app\streamlit_app.py
```

Streamlit will open the application in your browser.

Select:

```text
Extraction Provider
        ↓
Ollama
        ↓
llama3.1:8b
```

Upload one or more research papers.

Then click:

```text
🚀 Extract Data From All Papers
```

---

# 🔑 OpenAI Setup

OpenAI can also be used as an extraction provider.

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_model_here
OLLAMA_MODEL=llama3.1:8b
```

**Never commit `.env` to GitHub.**

The `.gitignore` file already excludes it.

---

# 📁 Output

The application provides two main outputs.

## JSON

Contains the complete structured extraction:

```text
microplastic_extraction.json
```

This preserves nested information such as endpoints and evidence.

---

## CSV

A simplified tabular dataset:

```text
microplastic_experiments.csv
```

Example:

| Polymer | Treatment | Temperature |   pH | Duration | Initial Mass | Final Mass |
| ------- | --------- | ----------: | ---: | -------: | -----------: | ---------: |
| PS      | Plasma    |          25 | null |        2 |          100 |         82 |
| PE      | Oxidation |          30 |    7 |       24 |           50 |         45 |

---

# 🔎 Provenance

Scientific data should be traceable back to its original source.

The project therefore attempts to preserve:

```text
Source PDF
    ↓
Page
    ↓
Table/Figure
    ↓
Evidence text
    ↓
Extracted value
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

This makes later manual verification possible.

---

# 📚 Research Dataset Design

The eventual dataset is intended to contain **one record per distinct experimental condition**.

For example, if a paper tests:

```text
PS + Treatment A
PS + Treatment B
PS + Treatment C
```

these should become three separate experimental records rather than one combined record.

This is important for later machine-learning analysis.

---

# 🤖 Future Machine Learning Pipeline

The extraction project is the first stage of a larger research pipeline.

The planned architecture is:

```text
                RESEARCH PAPERS
                       │
                       ▼
                 PDF Extraction
                       │
                       ▼
                  AI Extraction
                       │
                       ▼
              Structured Experiments
                       │
                       ▼
             Evidence + Provenance
                       │
                       ▼
                 Normalization
                       │
                       ▼
                  Validation
                       │
                       ▼
                Research Dataset
                       │
                       ▼
              Exploratory Analysis
                       │
                       ▼
              Feature Engineering
                       │
                       ▼
                ML Development
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Degradation          Treatment
        Prediction          Optimization
```

Potential ML targets include:

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

# 🧪 Planned Research Features

The current version is an initial extraction pipeline.

Future versions are planned to include:

### PDF Processing

* [ ] Better scanned-PDF support
* [ ] OCR
* [ ] Table extraction
* [ ] Figure extraction
* [ ] Supplementary-information extraction
* [ ] Page-level provenance

### Scientific Extraction

* [ ] Molecular-weight information
* [ ] Surface-area changes
* [ ] Carbonyl index
* [ ] Crystallinity
* [ ] Particle-size distribution
* [ ] TOC/CO₂ mineralization
* [ ] Chemical characterization
* [ ] SEM information
* [ ] FTIR information
* [ ] XPS information
* [ ] GC-MS information
* [ ] GPC information

### Dataset

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

### Machine Learning

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

The current Ollama implementation primarily extracts the **text layer** of PDFs.

Therefore, it may have difficulty with:

* scanned PDFs
* image-only pages
* complicated tables
* graphs
* chemical structures
* information contained only in figures
* supplementary information
* equations
* multi-column extraction errors

A future version will incorporate specialized table extraction and vision-based processing.

---

# 🔬 Scientific Reliability

This project is intended as a **research-assistance and data-curation tool**, not as a replacement for manual scientific verification.

AI-generated extraction should be checked against the original paper before the data is used for:

* publication
* statistical analysis
* machine-learning training
* scientific conclusions

The project prioritizes:

```text
Accuracy
   >
Completeness
   >
Automation
```

A missing value represented as `null` is preferable to an invented value.

---

# 🔐 Data and Privacy

Do not upload confidential or unpublished research papers to external AI services without appropriate authorization.

When using Ollama, the model runs locally.

When using an external API provider, the paper content is processed through that provider's API according to its applicable terms and policies.

---

# 📜 License

This project is currently under development for research and educational purposes.

A formal open-source license can be added when the project reaches a stable release.

---

# 👨‍🔬 Project Context

This project is being developed as part of research planning around:

**Microplastic degradation, environmental chemistry, scientific data extraction, and machine learning.**

The long-term research direction is to combine:

```text
Chemistry
+
Environmental Science
+
Scientific Literature Mining
+
Machine Learning
+
Computational Modeling
```

to investigate how different microplastic polymers respond to different degradation and treatment conditions.

---

# ⭐ Project Status

**Current stage:** Active development

### Current working components

* [x] Streamlit interface
* [x] Multiple PDF upload
* [x] Ollama integration
* [x] OpenAI integration
* [x] Pydantic structured schema
* [x] Basic normalization
* [x] Basic validation
* [x] JSON export
* [x] CSV export
* [x] Evidence/provenance fields

### In development

* [ ] Better table extraction
* [ ] Figure/graph extraction
* [ ] OCR
* [ ] Improved scientific validation
* [ ] Larger literature dataset
* [ ] ML-ready feature engineering
* [ ] Degradation prediction model

---

# 📌 Important Principle

> **The goal is not simply to extract more data. The goal is to build a traceable, scientifically defensible dataset that can support reliable downstream analysis and machine learning.**

---

## Author

**Sidhant Patel**

BS Chemical Science
Indian Institute of Technology Mandi

Research interests:

* Microplastic degradation
* Environmental chemistry
* Green chemistry
* Computational chemistry
* Machine learning for chemistry
* Scientific data extraction
* AI-assisted scientific research
