# Microplastic Degradation Data Extractor Using AI

This project reads research-paper PDFs and turns the experimental information about
microplastic degradation into structured JSON and CSV files. It is designed to help a
researcher build a clean, reviewable dataset without losing the evidence behind each
number.

The application uses the OpenAI Responses API for extraction. It does not replace
scientific review: every extracted experiment should be checked against the paper
before it is used for analysis or machine learning.

## What the project does

The complete workflow is:

```text
PDF
	-> upload the PDF to the OpenAI API
	-> ask the model for structured experiment records
	-> enforce the expected JSON shape with Pydantic
	-> normalize common names and calculate helpful derived fields
	-> check values with scientific sanity rules
	-> show records and evidence in Streamlit
	-> download JSON and CSV
```

One paper can contain many experiments. For example, different polymers, treatment
conditions, temperatures, durations, or time points become separate experiment
records rather than being merged together.

## Project layout

```text
microplastic-degradation-data-extractor-ai/
|-- app/
|   `-- streamlit_app.py       Web interface for uploading and reviewing PDFs
|-- data/
|   |-- database/              Reserved for database files
|   |-- extracted/              JSON output location
|   |-- processed/              CSV or processed dataset location
|   |-- raw/papers/             Uploaded PDFs used during extraction
|   `-- papers/                 Paper-related working data
|-- src/
|   |-- normalization.py       Standard names and derived values
|   |-- openai_extractor.py    OpenAI upload and Responses API call
|   |-- prompt.py              Scientific extraction instructions
|   |-- schemas.py              Pydantic data model and field definitions
|   `-- validation.py           Value checks and warnings
|-- tests/
|   |-- test_normalization.py  Normalization tests
|   `-- test_validation.py     Validation tests
|-- requirements.txt           Python dependencies
|-- run_cli.py                 Command-line extraction interface
`-- README.md                  This documentation
```

## Requirements

- Python 3.10 or newer is recommended.
- An OpenAI API key with access to the model you choose.
- A research-paper PDF with selectable text is recommended. Scanned PDFs and
	graph-only results may need additional OCR or digitization work.

## Installation on Windows PowerShell

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can run the environment's Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configure the API key

Copy `.env.example` to a new file named `.env`:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and provide your credentials and model:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_available_model_name
```

Both the Streamlit application and the CLI load these values from `.env`. The API
key can also be supplied as an environment variable. Never commit `.env` or share
the key. The repository's `.gitignore` already excludes it.

The model shown in `.env.example` is only an example. Replace it with a model that
is available to your OpenAI account. You can also select a model in the Streamlit
interface or pass one to the CLI.

## Run the Streamlit application

Start the web interface with:

```powershell
streamlit run app/streamlit_app.py
```

Then:

1. Open the local URL printed by Streamlit.
2. Upload one or more PDF files.
3. Confirm the selected filenames and sizes.
4. Enter the OpenAI model if needed.
5. Click **Extract data from all papers**.
6. Review the experiment table, validation messages, and evidence panels.
7. Download the JSON and CSV results.

Each uploaded PDF is temporarily saved under `data/raw/papers/` before it is sent
to the API. Extraction errors for one paper are displayed and collected so the
other selected papers can continue processing.

## Run one PDF from the command line

The CLI is useful for scripts, batch jobs, or users who do not need the web UI:

```powershell
python run_cli.py path\to\paper.pdf --output data\extracted\paper.json
```

Choose a model explicitly when needed:

```powershell
python run_cli.py path\to\paper.pdf `
	--output data\extracted\paper.json `
	--model your_available_model_name
```

The CLI writes a JSON file and prints the number of experiments, validation errors,
and warnings. It adds `validation_errors` and `validation_warnings` to the output.

## What is extracted

Each experiment may contain:

- Polymer and subtype, such as PE, PP, PS, PET, PVC, or PA/Nylon.
- Particle size range and shape.
- Treatment category and the specific treatment.
- Catalyst and catalyst concentration.
- Temperature, pH, and treatment duration.
- Initial and final mass.
- Multiple endpoints, including mass loss, TOC removal, mineralization,
	molecular-weight reduction, particle-size reduction, carbonyl index, or another
	endpoint explicitly reported by the paper.
- Evidence such as page, section, table, figure, supporting text, and confidence.
- The origin of a value: `reported`, `calculated`, `digitized_from_figure`,
	`inferred`, or `unknown`.

Missing values are represented as `null`. The extractor is instructed not to invent
values or treat a background statement as experimental evidence.

## Output data model

The top-level JSON object has this shape:

```json
{
	"paper_title": "Example paper title",
	"doi": "10.xxxx/example",
	"experiments": [],
	"extraction_notes": []
}
```

An experiment contains condition fields plus an `endpoints` list and an `evidence`
list. An endpoint stores its type, numeric value, unit, measurement method, value
origin, and optional evidence.

The CSV download is a review-friendly table. It includes the main condition fields
and combines endpoint names into one `endpoints` column. The complete evidence and
nested endpoint details are preserved in the JSON download, so keep the JSON as the
authoritative archive.

## How the code works

### `src/openai_extractor.py`

1. Checks that `OPENAI_API_KEY` exists.
2. Uploads the PDF with the OpenAI Files API.
3. Sends the PDF and the extraction instructions to the Responses API.
4. Supplies a strict JSON schema generated from `ExtractionResult`.
5. Parses the response and validates it with Pydantic.

### `src/prompt.py`

This is the scientific instruction set given to the model. It requires separate
records for distinct conditions, preserves endpoint meanings, requests evidence,
and prohibits invented values. Change this file carefully because prompt changes
can alter the dataset's behavior.

### `src/schemas.py`

This defines the allowed structure. `ExtractionResult` contains paper metadata and
experiments. `Experiment`, `Endpoint`, and `Evidence` define the fields and types
that the model must return.

### `src/normalization.py`

This converts common polymer names to abbreviations, for example `polystyrene` to
`PS`, and maps treatment synonyms to consistent categories. It also calculates:

- `duration_days` from `duration_h`.
- `rate_percent_day` for a mass-loss endpoint when mass loss and duration are
	available.

Calculated fields should still be reviewed against the paper and the extraction
assumptions.

### `src/validation.py`

This performs sanity checks after normalization:

- Temperature cannot be below absolute zero.
- pH outside 0 to 14 produces a warning.
- Mass values cannot be negative.
- Final mass greater than initial mass produces a warning for review.
- Percentage-style endpoints must be between 0 and 100.

Errors indicate values that should not be accepted without correction. Warnings may
be scientifically possible but deserve verification in the source paper.

### `app/streamlit_app.py`

This module connects the pieces. It accepts multiple PDFs, shows progress, stores
the combined results in Streamlit session state, displays validation messages and
evidence, and provides JSON/CSV download buttons.

### `run_cli.py`

This runs the same extraction, normalization, and validation pipeline for one PDF
without Streamlit. It is the simplest entry point for automation.

## Scientific review guidance

The application is an extraction assistant, not an automatic approval system.
Before using a record:

1. Open the source paper and verify each important number.
2. Check that the record represents the correct polymer, treatment, and time point.
3. Confirm that the endpoint meaning was preserved. Mass loss is not the same as
	 mineralization.
4. Read the page, table, figure, and evidence text when available.
5. Treat `inferred` and `digitized_from_figure` values as requiring extra review.
6. Keep records with unresolved errors out of an ML training dataset.

A practical first evaluation is to extract about 10 papers, manually label the
correct values, and measure field-level accuracy before scaling up.

## Run the tests

From the project folder:

```powershell
python -m pytest
```

The tests currently cover polymer normalization, derived duration, and detection
of an invalid percentage endpoint. Add tests when changing the schema, prompt,
normalization rules, or validation rules.

## Troubleshooting

### `OPENAI_API_KEY is missing`

Create `.env` from `.env.example`, add a valid key, and restart Streamlit. Make sure
the terminal is running from the project folder.

### Model or API errors

Check that the model name is available to your account and that your API account can
upload files and use the Responses API. Try passing the model explicitly with the
CLI or entering it in Streamlit.

### No useful values are extracted

Check whether the PDF contains selectable text. Image-only scans, complicated
tables, and graph-only measurements may require OCR, table extraction, or a future
vision/digitization step.

### Validation messages appear

The messages do not automatically prove that the paper is wrong. They identify
values that need a human check, such as an unusual pH or final mass greater than
initial mass.

## Limitations and privacy

- The original PDF is sent to the configured OpenAI API provider for processing.
- Extraction quality depends on PDF text, tables, figures, and the selected model.
- V1 does not perform reliable graph digitization or full OCR for scanned papers.
- Uploaded PDFs are written locally under `data/raw/papers/`; generated data files
	may be written under `data/extracted/` or `data/processed/`.
- Keep papers and API credentials subject to your institution's privacy and data
	handling requirements.
