import streamlit as st
import pandas as pd
import duckdb
import io

csv = '''
Beverage,Price
Orange juice,2
Expresso,2
Tea,3
'''

beverages = pd.read_csv(io.StringIO(csv))
beverages = pd.DataFrame(beverages)

csv2 = '''
Food_item,Food_price
Cookie,2
Chocolatine,2
Muffin,3
'''

food_items = pd.read_csv(io.StringIO(csv2))
food_items = pd.DataFrame(food_items)


st.title("SQL SRS")
st.header("Spaced Repetion System SQL practice")

with st.sidebar:
    option = st.selectbox(
        "What would you like to review would you like to review ?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme",)

    st.write("You selected:", option)

answer = f"""
SELECT * FROM beverages \n
CROSS JOIN food_items
"""


user_query = st.text_area(label="Enter your query :", placeholder="Your SQL code...")
if user_query:
    result = duckdb.query(user_query)
    st.dataframe(result)


    st.write("Expected result :")
    solution = duckdb.query(answer).df()
    st.write(solution)

tab1,tab2 = st.tabs(["Tables","Solution"])

with tab1:
    st.write("beverages")
    st.dataframe(beverages)
    st.write("food_items")
    st.dataframe(food_items)

with tab2:
    st.write(answer)




