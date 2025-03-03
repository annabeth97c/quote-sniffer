import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.title("🔍 QuoteSniffer")

st.sidebar.header("Upload Files")
uploaded_files = st.sidebar.file_uploader("Upload text or Word documents", accept_multiple_files=True)

# Parameters
passage_length = st.sidebar.slider("Passage Length", min_value=10, max_value=100, value=20, step=1, help="Number of words in passages. Documents are split into chunks with selected number of words. Comparison is done on said chunks")
minhash_threshold = st.sidebar.slider("Similarity Threshold", min_value=0.1, max_value=1.0, value=0.5, step=0.02, help="Similarity threshold used by Locality Sensitive Hashing algorithm")
num_perm = st.sidebar.slider("Number of Permutations", min_value=64, max_value=1024, value=128, step=32, help="Number of permutations used by Locality Sensitive Hashing algorithm")
sim_score_threshold = st.sidebar.slider("Final Similarity Score Threshold", min_value=0.1, max_value=1.0, value=0.2, step=0.1, help="Jaccard score threshold to confirm match performance and threshold the matches that are shown")

if st.sidebar.button("Find Similar Passages") and uploaded_files:
    with st.spinner("Processing..."):
        files = [("files", (file.name, file.getvalue())) for file in uploaded_files]
        params = {"passage_length": passage_length, "threshold": minhash_threshold, "num_perm": num_perm, "sim_score_threshold": sim_score_threshold}
        
        response = requests.post("http://127.0.0.1:8000/find_similarities/", files=files, params=params)
        if response.status_code == 200:
            result = response.json()
            similar_passages = result["similar_passages"]

            if similar_passages:
                st.success(f"Found {len(similar_passages)} similar passages!")
                df = pd.DataFrame(similar_passages)
                st.dataframe(df)

                for pair in similar_passages:
                    col1, col2 = st.columns(2)

                    score_marker = "🙃"
                    if pair['score'] < 0.3:
                        score_marker = "💔"
                    elif pair['score'] < 0.6:
                        score_marker = "🍯"
                    elif pair['score'] >= 0.6:
                        score_marker = "✨🍀✨"
                    with col1:
                        st.write(f"📜 **{pair['doc1']}**")
                        st.write(f"Passage {pair['passage1_index'] + 1} - W. {pair['passage1_index']*passage_length} to {(pair['passage1_index'] + 1)*passage_length} - Similarity: " + score_marker)
                        st.markdown(f"<div style='background-color:#999999;padding:10px'>{pair['text1']}</div>", unsafe_allow_html=True)
                        st.write("")
                    with col2:
                        st.write(f"📜 **{pair['doc2']}**")
                        st.write(f"Passage {pair['passage2_index'] + 1} - W. {pair['passage2_index']*passage_length} to {(pair['passage2_index'] + 1)*passage_length} ")
                        st.markdown(f"<div style='background-color:#999999;padding:10px'>{pair['text2']}</div>", unsafe_allow_html=True)
                        st.write("")
            else:
                st.warning("No similar passages found.")
        else:
            st.error("Error processing the files.")

st.sidebar.markdown("---")
st.sidebar.write("Built for Humanities Computing Jan'25")
st.sidebar.write("For any issues contact @annabeth97c 🙃💔")

