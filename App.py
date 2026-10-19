import streamlit as st
import json

st.title("🔧 BMET Knowledge-Base Assistant (V1)")
st.write("Grounding technical troubleshooting & manual references with exact citations.")

# Load database index
@st.cache_data
def load_index():
    with open("bmet_v1_index.json", "r") as f:
        return json.load(f)

try:
    index = load_index()
except Exception as e:
    st.error(f"Error loading index: {e}")
    index = []

def search_index(query, index):
    query_lower = query.lower().strip()
    words = [w for w in query_lower.split() if w not in ["error", "errors", "issue", "fault", "problem"]]
    
    if not words:
        words = query_lower.split()

    scored_results = []

    for item in index:
        text_content = (item["section"] + " " + item["text"]).lower()
        score = 0
        
        # Exact full phrase match gets highest priority
        if query_lower in text_content:
            score += 10
            
        # Match primary keywords
        for word in words:
            if word in text_content:
                score += 3
                
        if score > 0:
            scored_results.append((score, item))
            
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored_results]

query = st.text_input("Enter your BMET troubleshooting or maintenance query:")

if st.button("Search & Generate"):
    if query:
        results = search_index(query, index)
        st.success(f"Retrieved {len(results)} relevant source sections.")
        
        st.subheader("📋 Retrieved Source Context & Citations")
        if results:
            for item in results:
                with st.expander(f"Page {item['page']} — Section: {item['section']}"):
                    st.write(item["text"])
                    st.caption(f"Source Document ID: `{item['doc_id']}` | Page `{item['page']}`")
        else:
            st.warning("No matching manual sections found for this query.")
    else:
        st.info("Please enter a query to search.")
