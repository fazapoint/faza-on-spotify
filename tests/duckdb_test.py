import duckdb

# 1. Connect to an in-memory database
conn = duckdb.connect(database=':memory:')

# 2. Run a simple query
result = conn.execute("SELECT 42 AS answer").fetchall()

# 3. Verify the output
print(f"Connection successful! Test query result: {result}")
assert result == [(42,)], "DuckDB did not return the expected result."

# query = "SELECT * FROM test_data.csv"

# duckdb.sql(query).show()


#duckdb relation
# This does NOT load the data into memory yet. It creates a "Relation" (blueprint).
query_rel = duckdb.sql("SELECT * FROM 'test_data.csv'")

# Register it as a temporary view (The Spark equivalent)
duckdb.register("my_data", query_rel)

# Query it globally using that view name
duckdb.sql("SELECT count(*) FROM my_data").show()


# You can chain operations on it later, exactly like Spark
filtered_rel = query_rel.filter("DealerName = 'BINA MOTOR'").select("DealerName, DocumentNumber, created")

# The data is only processed when you trigger an action
filtered_rel.show()