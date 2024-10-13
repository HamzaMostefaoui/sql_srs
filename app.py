# pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
Beverage,Price
Orange juice,2
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))
beverages = pd.DataFrame(beverages)

CSV2 = """
Food_item,Food_price
Cookie,2
Chocolatine,2
Muffin,3
"""

food_items = pd.read_csv(io.StringIO(CSV2))
food_items = pd.DataFrame(food_items)


st.title("SQL SRS")
st.header("Spaced Repetion System SQL practice")

with st.sidebar:
    option = st.selectbox(
        "What would you like to review would you like to review ?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme",
    )

    st.write("You selected:", option)

ANSWER_STR = """
SELECT * FROM beverages \n
CROSS JOIN food_items
"""

solution_df = duckdb.query(ANSWER_STR).df()


user_query = st.text_area(label="Enter your query :", placeholder="Your SQL code...")
if user_query:
    result = duckdb.query(user_query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_differences = result.shape[0] - solution_df.shape[0]
    if result.shape[0] != solution_df.shape[0]:
        st.write(
            f"Your result has {n_lines_differences} lines differences with the solution   "
        )


tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    st.write("beverages")
    st.dataframe(beverages)
    st.write("food_items")
    st.dataframe(food_items)

with tab2:
    st.write(ANSWER_STR)
