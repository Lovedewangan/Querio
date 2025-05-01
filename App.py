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
st.title("📊 Querio")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df)

    # Use the original file name (without extension) as the table name
    table_name = os.path.splitext(uploaded_file.name)[0]
    st.session_state["table_name"] = table_name

    # Load CSV into in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    df.to_sql(table_name, conn, index=False, if_exists="replace")

    # Schema for prompt
    column_info = ", ".join(df.columns)
    prompt_template = f"""
You are an expert data analyst. Convert the following English question into a valid SQLite SQL query.
The table name is `{table_name}` and the columns are: {column_info}.

ONLY return the SQL query (no markdown, no explanation, no extra words).
Example:
Q: How many rows are there?
A: SELECT COUNT(*) FROM {table_name};
"""

    # Session state setup
    if "sql_query" not in st.session_state:
        st.session_state.sql_query = ""

    if "nl_query" not in st.session_state:
        st.session_state.nl_query = ""

    def generate_query():
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([prompt_template, st.session_state.nl_query])
        st.session_state.sql_query = response.text.strip().strip("`").strip()

    st.subheader("Write or Generate SQL Query")
    st.markdown(f"**🗂️ Table created: `{table_name}`**")

    st.text_area("✍️ SQL Query", key="sql_query", height=150)

    st.text_input("💬 Ask in natural language", key="nl_query", on_change=generate_query, placeholder="e.g., Show average age per department")

    st.button("🔄 Generate SQL from Natural Language", on_click=generate_query)

    if st.button("▶️ Run SQL") or st.session_state.get("auto_run", False):
        try:
            result = pd.read_sql_query(st.session_state.sql_query, conn)
            st.subheader("Query Result")
            if not result.empty:
                st.dataframe(result)
            else:
                st.write("No results found.")
        except sqlite3.Error as e:
            st.error(f"❌ Error executing SQL query: {e}")
