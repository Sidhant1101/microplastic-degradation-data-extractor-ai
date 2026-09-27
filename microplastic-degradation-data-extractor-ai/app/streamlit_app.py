import json
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")
if not os.getenv("OPENAI_API_KEY"):
    load_dotenv(Path(__file__).resolve().with_name(".env"))

from src.openai_extractor import extract_pdf
from src.normalization import normalize_result
from src.validation import validate_result

st.set_page_config(page_title="Microplastic AI Extractor", layout="wide")
st.title("Microplastic Degradation AI Extractor")
st.caption("PDF → structured experiments → evidence → validation → CSV/JSON")

if not os.getenv("OPENAI_API_KEY"):
    st.warning("OPENAI_API_KEY is not configured. Add it to .env before extraction.")

model = st.text_input("OpenAI model", os.getenv("OPENAI_MODEL", "gpt-5.6-luna"))
uploads = st.file_uploader(
    "Upload research-paper PDFs",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploads:
    st.success(f"{len(uploads)} paper(s) selected.")
    for upload in uploads:
        st.write(f"{upload.name} ({upload.size / 1024:.1f} KB)")

    if st.button("Extract data from all papers", type="primary", disabled=not bool(os.getenv("OPENAI_API_KEY"))):
        temp_dir = ROOT / "data" / "raw" / "papers"
        temp_dir.mkdir(parents=True, exist_ok=True)
        all_experiments = []
        all_errors = []
        all_warnings = []
        total = len(uploads)
        progress_bar = st.progress(0, text=f"Processing 0/{total} papers")

        for index, upload in enumerate(uploads):
            st.write(f"Processing {index + 1}/{total}: {upload.name}")
            st.divider()
            st.subheader(f"Processing: {upload.name}")

            with st.spinner(f"Extracting data from {upload.name}..."):
                try:
                    pdf_path = temp_dir / upload.name
                    pdf_path.write_bytes(upload.getvalue())
                    result = extract_pdf(str(pdf_path), model=model)
                    data = normalize_result(result.model_dump())
                    errors, warnings = validate_result(data)
                    all_experiments.extend(data.get("experiments", []))
                    all_errors.extend(errors)
                    all_warnings.extend(warnings)
                    st.success(
                        f"Completed: {upload.name} "
                        f"({len(data.get('experiments', []))} experiment(s) extracted)."
                    )
                except Exception as exc:
                    all_errors.append(f"{upload.name}: extraction failed: {exc}")
                    st.error(f"Extraction failed for {upload.name}: {exc}")
                finally:
                    completed = index + 1
                    progress_bar.progress(
                        completed / total,
                        text=f"Processed {completed}/{total} papers",
                    )

        st.session_state["data"] = {"experiments": all_experiments}
        st.session_state["errors"] = all_errors
        st.session_state["warnings"] = all_warnings
        st.success(
            f"Finished processing {len(uploads)} paper(s). "
            f"Total experiments extracted: {len(all_experiments)}"
        )

if "data" in st.session_state:
    data = st.session_state["data"]
    errors = st.session_state["errors"]
    warnings = st.session_state["warnings"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Experiments", len(data.get("experiments", [])))
    c2.metric("Validation errors", len(errors))
    c3.metric("Warnings", len(warnings))

    if errors:
        st.error("Validation errors")
        for x in errors:
            st.write("-", x)
    if warnings:
        st.warning("Validation warnings")
        for x in warnings:
            st.write("-", x)

    st.subheader("Extracted experiments")
    rows = []
    for idx, exp in enumerate(data.get("experiments", []), start=1):
        rows.append({
            "experiment": idx,
            "polymer": exp.get("polymer"),
            "treatment": exp.get("treatment_category"),
            "specific treatment": exp.get("treatment_specific"),
            "temperature C": exp.get("temperature_c"),
            "pH": exp.get("pH"),
            "duration h": exp.get("duration_h"),
            "initial mass mg": exp.get("initial_mass_mg"),
            "final mass mg": exp.get("final_mass_mg"),
            "endpoints": "; ".join(e.get("endpoint_type", "") for e in exp.get("endpoints", [])),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.subheader("Evidence / provenance")
    for i, exp in enumerate(data.get("experiments", []), start=1):
        with st.expander(f"Experiment {i}: {exp.get('polymer') or 'unknown polymer'}"):
            st.json({"experiment": exp})

    st.subheader("Download")
    json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
    st.download_button("Download JSON", json_bytes, "microplastic_extraction.json", "application/json")
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "microplastic_experiments.csv", "text/csv")
