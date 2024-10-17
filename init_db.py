import io
import pandas as pd
import duckdb


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES
# ------------------------------------------------------------

data = {
    "theme": ["cross_joins","cross_joins","group_by","window_functions"],
    "exercise_name": ["beverages_and_food","clothes_combination","sales_by_cust","wages_over"],
    "tables": [["beverages","food_items"],["sizes","trademarks"],["customer_sales"],["wages"]],
    "last_reviewed": ["1970-01-01","1970-01-01","1970-01-01","1970-01-01"],
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
Reebok
Asphalte
Abercrombie
Lewis
"""

trademarks = pd.read_csv(io.StringIO(TRADEMARKS_CSV))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks ")

# ------------------------------------------------------------
# GROUP BY EXERCISES
# ------------------------------------------------------------


clients = ["Oussama", "Julie", "Chris", "Tom", "Jean-Nicolas", "Aline", "Ben", "Toufik", "Sylvie", "David"]
ventes = [110, 49, 65, 23, 24, 3.99, 29, 48.77, 44, 10, 60, 12, 62, 19, 75] * 2

customer_sales = pd.DataFrame(ventes)
customer_sales.columns = ["sales"]
customer_sales["customer"] = clients * 3

con.execute("CREATE TABLE IF NOT EXISTS customer_sales AS SELECT * FROM customer_sales ")

# ------------------------------------------------------------
# WINDOW FUNCTION EXERCISES
# ------------------------------------------------------------

salary_data = {
    'name': ['Toufik', 'Jean-Nicolas', 'Daniel', 'Kaouter', 'Sylvie',
             'Sebastien', 'Diane', 'Romain', 'François', 'Anna',
             'Zeinaba', 'Gregory', 'Karima', 'Arthur', 'Benjamin'],
    'wage': [60000, 75000, 55000, 100000, 70000,
             90000, 65000, 100000, 68000, 85000,
             100000, 120000, 95000, 83000, 110000],
    'department': ['IT', 'HR', 'SALES', 'IT', 'IT',
                   'HR', 'SALES', 'IT', 'HR', 'SALES',
                   'IT', 'IT', 'HR', 'SALES', 'CEO'],
    'sex': ['H', 'H', 'H', 'F', 'F',
           'H', 'F', 'H', 'H', 'F',
           'F', 'H', 'F', 'H', 'H',]
}
wages = pd.DataFrame(salary_data)

con.execute("CREATE TABLE IF NOT EXISTS wages AS SELECT * FROM wages ")




con.close()


