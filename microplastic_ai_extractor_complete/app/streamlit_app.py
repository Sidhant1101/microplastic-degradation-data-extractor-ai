import json, os, sys
from pathlib import Path
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT)); load_dotenv(ROOT/'.env')
from src.groq_extractor import extract_pdf
from src.normalization import normalize_result
from src.validation import validate_result
st.set_page_config(page_title='Microplastic AI Extractor',layout='wide')
st.title('Microplastic Degradation AI Extractor')
st.caption('PDF → structured experiments → evidence → validation → CSV/JSON')
st.info('Groq mode sends extracted PDF text to the Groq API.')
if not os.getenv('GROQ_API_KEY'): st.warning('GROQ_API_KEY is not configured. Add it to .env before extracting.')
model=st.text_input('Groq model',os.getenv('GROQ_MODEL','llama-3.3-70b-versatile')); disabled=not bool(os.getenv('GROQ_API_KEY'))
files=st.file_uploader('Upload research-paper PDFs',type=['pdf'],accept_multiple_files=True)
if files:
    st.success(f'{len(files)} paper(s) selected.')
    for f in files: st.write(f'📄 **{f.name}** ({f.size/1024:.1f} KB)')
    if st.button('🚀 Extract Data From All Papers',type='primary',disabled=disabled):
        temp=ROOT/'data/raw/papers'; temp.mkdir(parents=True,exist_ok=True); exps=[]; errs=[]; warns=[]
        for f in files:
            st.divider(); st.subheader(f'Processing: {f.name}'); path=temp/f.name; path.write_bytes(f.getvalue())
            with st.spinner(f'Extracting data from {f.name}...'):
                try:
                    result=extract_pdf(str(path),model=model); data=normalize_result(result.model_dump()); e,w=validate_result(data)
                    for x in data.get('experiments',[]): x['source_file']=f.name
                    exps.extend(data.get('experiments',[])); errs.extend([f'{f.name}: {x}' for x in e]); warns.extend([f'{f.name}: {x}' for x in w])
                    st.success(f'✅ Completed: {f.name} — {len(data.get("experiments",[]))} experiment(s) extracted.')
                except Exception as exc: st.error(f'❌ Extraction failed for {f.name}: {exc}')
        st.session_state['data']={'experiments':exps}; st.session_state['errors']=errs; st.session_state['warnings']=warns
        st.success(f'🎉 Finished processing {len(files)} paper(s). Total experiments extracted: {len(exps)}')
if 'data' in st.session_state:
    data=st.session_state['data']; errors=st.session_state['errors']; warnings=st.session_state['warnings']; st.divider(); st.subheader('Extraction Summary')
    c1,c2,c3=st.columns(3); c1.metric('Experiments',len(data.get('experiments',[]))); c2.metric('Validation errors',len(errors)); c3.metric('Warnings',len(warnings))
    if errors:
        st.error('Validation errors'); [st.write('-',x) for x in errors]
    if warnings:
        st.warning('Validation warnings'); [st.write('-',x) for x in warnings]
    rows=[]
    for i,e in enumerate(data.get('experiments',[]),1): rows.append({'experiment':i,'source file':e.get('source_file'),'polymer':e.get('polymer'),'treatment':e.get('treatment_category'),'specific treatment':e.get('treatment_specific'),'temperature C':e.get('temperature_c'),'pH':e.get('pH'),'duration h':e.get('duration_h'),'initial mass mg':e.get('initial_mass_mg'),'final mass mg':e.get('final_mass_mg'),'endpoints':'; '.join(x.get('endpoint_type','') for x in e.get('endpoints',[]))})
    df=pd.DataFrame(rows); st.subheader('Extracted Experiments'); st.dataframe(df,use_container_width=True) if not df.empty else st.info('No experiments were extracted.')
    st.subheader('Evidence / Provenance')
    for i,e in enumerate(data.get('experiments',[]),1):
        with st.expander(f'Experiment {i}: {e.get("polymer") or "unknown polymer"}'): st.json({'experiment':e})
    st.subheader('Download'); st.download_button('⬇️ Download JSON',json.dumps(data,indent=2,ensure_ascii=False).encode(),'microplastic_extraction.json','application/json'); st.download_button('⬇️ Download CSV',df.to_csv(index=False).encode(),'microplastic_experiments.csv','text/csv')
