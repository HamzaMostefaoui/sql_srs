import streamlit as st
import pandas as pd
import duckdb

st.title("_Let's practice SQL questions_ !")

data = {"a":[1, 2, 3], "b":[4, 5, 6]}
df = pd.DataFrame(data)

sql_query = st.text_area(label="Enter your query :")
result = duckdb.query(sql_query)
st.dataframe(result)


