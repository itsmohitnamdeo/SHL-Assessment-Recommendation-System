import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.markdown("<h1 style='text-align:center;'>🤖 SHL Assessment Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Enter a query or a job description and get matching assessments</p>", unsafe_allow_html=True)

query = st.text_area("🔍 Enter your query:", placeholder="e.g. Looking for a test to evaluate critical thinking for entry-level hires")

if st.button("🔎 Get Recommendations"):
    if query.strip(): 
        try:
            with st.spinner("Fetching recommendations..."):
                # For local development, replace the URL with "http://localhost:8000/recommend" 
                res = requests.post("https://shl-assessment-recommendation-system-xx1e.onrender.com/recommend", json={"query": query})
            if res.status_code == 200:
                data = res.json()
                recommended_assessments = data.get("recommended assessments", [])
                if recommended_assessments:
                    st.success(f"Top {len(recommended_assessments)} recommendations found!")
                    df = pd.DataFrame(recommended_assessments)
                    st.dataframe(df)
                else:
                    st.warning("No recommendations found.")
            else:
                st.error(f"API Error: {res.status_code}")
        except Exception as e:
            st.error(f"Error connecting to API: {e}")
    else:
        st.warning("Please enter a valid query.")
