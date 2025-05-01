from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import sqlite3
import os
import google.generativeai as genai

# Load API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI SQL from CSV")
st.title("📊 AI-Powered SQL Query Engine from CSV")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df)


    # Load CSV into in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    df.to_sql("uploaded_data", conn, index=False, if_exists="replace")

    # Extract schema
    column_info = ", ".join([f"{col}" for col in df.columns])
    prompt = f"""
You are an expert data analyst. Convert the following English question into a valid SQLite SQL query.
The table name is `uploaded_data` and the columns are: {column_info}.

ONLY return the SQL query (no markdown, no explanation, no extra words).
Example:
Q: How many rows are there?
A: SELECT COUNT(*) FROM uploaded_data;
"""

    question = st.text_input("Ask a question about your data:")

    # Check if SQL query is already in session state
    if "sql_query" not in st.session_state:
        st.session_state.sql_query = ""

    if st.button("Generate SQL"):
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([prompt, question])
        sql_query = response.text.strip().strip("`").strip()

        # Store the generated SQL query in session state
        st.session_state.sql_query = sql_query

        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")

    if st.session_state.sql_query:  # Check if there's a stored SQL query
        if st.button("Run SQL"):
            try:
                # Execute the query
                result = pd.read_sql_query(st.session_state.sql_query, conn)
                st.subheader("Query Result")
                if not result.empty:
                    st.dataframe(result)
                else:
                    st.write("No results found.")
            except sqlite3.Error as e:
                st.error(f"❌ Error executing SQL query: {e}")
