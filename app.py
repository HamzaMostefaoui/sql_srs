# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
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


    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercise)
    exercise_name = exercise.loc[0, 'exercise_name']
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()


user_query = st.text_area(label="Enter your query :", placeholder="Your SQL code...")
if user_query:
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_differences = result.shape[0] - solution_df.shape[0]
    if result.shape[0] != solution_df.shape[0]:
        st.write(f"Your result has {n_lines_differences} lines differences with the solution")

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    exercises_tables = exercise.loc[0,"tables"]
    for table in exercises_tables:
        df_table = con.execute(f"SELECT * FROM {table}")
        st.dataframe(df_table)


with tab2:
    exercise_name = exercise.loc[0,'exercise_name']
    with open(f"answers/{exercise_name}.sql","r") as f:
        answer = f.read()
    st.write(answer)

