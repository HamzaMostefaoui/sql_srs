import streamlit as st
import pandas as pd
import duckdb

st.title("SQL SRS")
st.header("Spaced Repetion System SQL practice")

with st.sidebar:
    option = st.selectbox(
        "What would you like to review would you like to review ?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme",)

    st.write("You selected:", option)




data = {"a":[1, 2, 3], "b":[4, 5, 6]}
df = pd.DataFrame(data)
sql_query = st.text_area(label="Enter your query :", placeholder="Your SQL code...")
result = duckdb.query(sql_query)
st.dataframe(result)


