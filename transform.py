import duckdb


# describe the json
# duckdb.sql("DESCRIBE SELECT * FROM read_json_auto('data/L1/spotify/*.json')").show()

query = """
WITH raw_data as (
    SELECT unnest(items) as entry
    FROM read_json_auto('data/L1/spotify/*.json') 
)

SELECT
    entry.played_at,
    entry.track.name as song_name,
    entry.track.artists[1].name as artist_name,
    entry.track.album.name
FROM raw_data
"""

duckdb.sql(query).show()