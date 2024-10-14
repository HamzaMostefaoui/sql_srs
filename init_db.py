import io
import pandas as pd
import duckdb


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES
# ------------------------------------------------------------

data = {
    "theme": ["cross_joins","cross_joins"],
    "exercise_name": ["beverages_and_food","clothes_combination"],
    "tables": [["beverages","food_items"],["sizes","trademarks"]],
    "last_reviewed": ["1980-01-01","1970-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")


# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------

BEVERAGES_CSV = """
Beverage,Price
Orange juice,2
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(BEVERAGES_CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages ")

FOOD_ITEMS_CSV = """
Food_item,Food_price
Cookie,2
Chocolatine,2
Muffin,3
"""

food_items = pd.read_csv(io.StringIO(FOOD_ITEMS_CSV))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items ")


SIZES_CSV = """
size
XS
M
L
XL
"""

sizes = pd.read_csv(io.StringIO(SIZES_CSV))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes ")

TRADEMARKS_CSV = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""

trademarks = pd.read_csv(io.StringIO(TRADEMARKS_CSV))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks ")

con.close()


