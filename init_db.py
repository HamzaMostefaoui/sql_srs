import io
import pandas as pd
import duckdb


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES
# ------------------------------------------------------------

data = {
    "theme": ["cross_joins","window_functions"],
    "exercise_name": ["beverages_and_food","simple_window"],
    "tables": [["beverages","food_items"],"simple_window"],
    "last_reviewed": ["1970-01-01","1970-01-01"]
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")


# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------

CSV = """
Beverage,Price
Orange juice,2
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages ")

CSV2 = """
Food_item,Food_price
Cookie,2
Chocolatine,2
Muffin,3
"""

food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items ")



