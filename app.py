# pylint: disable=missing-module-docstring

import io
from gettext import Catalog

import duckdb
import pandas as pd
import streamlit as st
import ast

from duckdb.duckdb import CatalogException, BinderException

con = duckdb.connect(database="data/exercises_sql_tables.duckdb",read_only=False)

#solution_df = duckdb.query(ANSWER_STR).df()

st.title("SQL SRS")
st.header("Spaced Repetion System SQL practice")

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review would you like to review ?",
        ("cross_joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)


user_query = st.text_area(label="Enter your query :", placeholder="Your SQL code...")
if user_query:
    try:
     result = con.execute(user_query)
     st.dataframe(result)
    except CatalogException as e:
        st.error("Unknown table please try again")
    except BinderException as e:
        st.error("Unknown column please try again")


#
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing")
#
#     n_lines_differences = result.shape[0] - solution_df.shape[0]
#     if result.shape[0] != solution_df.shape[0]:
#         st.write(
#             f"Your result has {n_lines_differences} lines differences with the solution   "
#         )
#
#
tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    exercises_tables = ast.literal_eval(exercise.loc[0,"tables"])
    for table in exercises_tables:
        df_table = con.execute(f"SELECT * FROM {table}")
        st.dataframe(df_table)


with tab2:
    exercise_name = exercise.loc[0,'exercise_name']
    with open(f"answers/{exercise_name}.sql","r") as f:
        answer = f.read()
    st.write(answer)

