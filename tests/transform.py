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
    entry.track.duration_ms as song_duration,
    entry.track.artists[1].name as artist_name, --need to adjust if theres more than one artists
    entry.track.album.name as album_name,
    entry.track.album.release_date as album_release_date,
    entry.context.type as source_played_from,
    entry.context.external_urls.spotify as source_played_from_link,
    entry.track.album.images[2].url as album_cover_url
FROM raw_data
"""
duckdb.sql(query).show()

# duckdb.sql(query).show(max_width=10000)