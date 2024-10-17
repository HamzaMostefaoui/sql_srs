# pylint: disable=missing-module-docstring

import os
import logging

import duckdb
import streamlit as st
from datetime import date, timedelta

# -------Creation of data folder-----------

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())


# -----------Functions-----------


def display_available_themes(connection):
    """
    Display all the themes that
    :param connection: connection to DB
    :return: selected_theme
    """
    available_themes = connection.execute("SELECT DISTINCT theme FROM memory_state")
    return available_themes


def display_exercise(connection, selected_theme=None):
    if selected_theme:
        memory_query = f"SELECT * FROM memory_state WHERE theme = '{selected_theme}' ORDER BY last_reviewed"
    else:
        memory_query = "SELECT * FROM memory_state ORDER BY last_reviewed"

    oldest_exercise_name = connection.execute(memory_query).df()
    exercise_name = oldest_exercise_name.loc[0, "exercise_name"]

    return exercise_name


def display_tables(connection, exercise):
    """
    Display tables corresponding to the oldest exercise of the selected theme,
    if no theme is selected the oldest one among all the themes is selected.
    """
    st.header("Tables:")

    memory_query = f"SELECT * FROM memory_state WHERE exercise_name = '{exercise}'"
    oldest_exercise_tables = connection.execute(memory_query).df()
    exercise_tables = oldest_exercise_tables.loc[0, "tables"]

    for table in exercise_tables:
        st.write(table)
        df_exercise_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_exercise_table)


def exercise_solution_df(connection, exercise_name):

    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()
    return solution_df


def exercise_solution_text(connection, exercise_name):
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    return st.write(answer)


def display_user_query(connection, user_query):
    result = connection.execute(user_query).df()
    return result


def user_query_validation(connection, user_query, exercise_name):
    user_result = display_user_query(connection, user_query)
    solution_df = exercise_solution_df(connection, exercise_name)

    try:
        user_result = user_result[solution_df.columns]
        comparison = user_result.compare(solution_df)
        st.dataframe(comparison)
        if comparison.shape == (0, 0):
            st.write("Correct!")
            st.balloons()
            repetion_system(exercise_name)
    except KeyError:
        st.error("Some columns are missing.")

    n_lines_difference = user_result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.error(
            f"Result has a {n_lines_difference} line(s) difference with the solution."
        )

    return user_result


def repetion_system(exercise_name):
    cols = st.columns(3)
    for i, n_days in enumerate([2, 7, 21]):
        with cols[i]:  # Place each button in its respective column
            if st.button(f"See again in {n_days} days"):
                next_review = date.today() + timedelta(days=n_days)
                con.execute(
                    f"UPDATE memory_state SET last_reviewed = {next_review} WHERE exercise_name = '{exercise_name}'",
                )
                st.rerun()

    if st.button("Reset"):
        con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
        st.rerun()


# -----------App------------

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

st.title("SQL SRS")
st.header("Spaced Repetion System")

with st.sidebar:
    user_selection = st.selectbox(
        "What would you like to review?",
        display_available_themes(con),
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"You selected {user_selection}")
user_exercise = display_exercise(con, user_selection)

with st.sidebar:
    display_tables(con, user_exercise)

form = st.form("my_form")
query = form.text_area(
    label="Type your code", placeholder="your SQL query...", key="user_input"
)
form.form_submit_button("Submit")


tab1, tab2, tab3 = st.tabs(["Your query", "Expected result", "Solution"])


with tab1:
    if query:
        user_query_validation(con, query, user_exercise)
        st.dataframe(display_user_query(con, query))


with tab2:
    st.dataframe(exercise_solution_df(con, user_exercise))

with tab3:

    st.warning("Did you tried your best before looking at it ?", icon="⚠️")
    on = st.toggle("See the solution")

    if on:
        exercise_solution_text(con, user_exercise)
