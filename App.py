import streamlit as st
import json
import re
from rank_bm25 import BM25Okapi

st.set_page_config(page_title="BMET Knowledge-Base Prototype (V1)", layout="wide")

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

@st.cache_resource
def load_engine():
    with open("bmet_v1_index.json", "r", encoding="utf-8") as f:
        index = json.load(f)
    corpus = [chunk['text'] for chunk in index]
    tokenized_corpus = [tokenize(doc) for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    return index, bm25

index, bm25 = load_engine()

st.title("🔧 BMET Knowledge-Base Assistant (V1)")
st.markdown("Query the Philips IntelliVue technical manual with strict source grounding and exact page citations.")

query = st.text_input("Enter your BMET troubleshooting or maintenance query:", "SpO2")

if st.button("Search & Generate"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        tokenized_query = tokenize(query)
        scores = bm25.get_scores(tokenized_query)
        scored_indices = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        
        top_chunks = []
        seen_pages = set()
        for idx, score in scored_indices:
            if score > 0:
                chunk = index[idx]
                if chunk['page_number'] not in seen_pages:
                    seen_pages.add(chunk['page_number'])
                    top_chunks.append(chunk)
            if len(top_chunks) >= 3:
                break
        
        if not top_chunks:
            st.error("The provided document does not state an answer to this query.")
        else:
            st.success(f"Retrieved {len(top_chunks)} relevant source sections.")
            st.markdown("### 📋 Retrieved Source Context & Citations")
            for tc in top_chunks:
                with st.expander(f"Page {tc['page_number']} — Section: {tc['section']}", expanded=True):
                    st.write(tc['text'])
                    st.caption(f"Source Document ID: `{tc['doc_id']}` | Page `{tc['page_number']}`")

