import streamlit as st
import json

st.set_page_config(page_title="BMET Knowledge-Base Prototype (V1)", layout="wide")

@st.cache_resource
def load_index():
    with open("bmet_v1_index.json", "r", encoding="utf-8") as f:
        return json.load(f)

index = load_index()

st.title("🔧 BMET Knowledge-Base Assistant (V1)")
st.markdown("Query the Philips IntelliVue technical manual with strict source grounding and exact page citations.")

query = st.text_input("Enter your BMET troubleshooting or maintenance query:", "ECG")

if st.button("Search & Generate"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        # Convert both query words AND the text to lowercase for reliable matching
        query_words = [w.lower() for w in query.split()]
        top_chunks = []
        
        for chunk in index:
            text_lower = chunk['text'].lower()
            section_lower = chunk['section'].lower()
            combined_text = text_lower + " " + section_lower
            
            if any(word in combined_text for word in query_words):
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
