import os
import polars as pl
import duckdb
from deltalake import DeltaTable, write_deltalake

# Define local storage paths
base_dir = os.path.dirname(os.path.abspath(__file__))
LANDING_PATH = os.path.abspath(os.path.join(base_dir, "..", "Warehouse", "Landing"))
L1_PATH = os.path.abspath(os.path.join(base_dir, "..", "Warehouse", "L1")) 

print(LANDING_PATH)
print(L1_PATH)

# Initialize an empty table if it doesnt exist
if not os.path.exists(L1_PATH):
    init_df = pl.DataFrame