CREATE OR REPLACE VIEW `gen-lang-client-0386264733.spotify_api_data.enriched_tracks` AS
SELECT
  st.track_id,
  st.track_name,
  st.artist_name,
  st.album_name,
  st.release_date,
  st.duration_ms,
  st.popularity,
  st.added_at,
  st.explicit,
  td.artist_genres,
  EXTRACT(YEAR FROM st.added_at) as added_year,
  EXTRACT(MONTH FROM st.added_at) as added_month
FROM `gen-lang-client-0386264733.spotify_api_data.saved_tracks` st
LEFT JOIN `gen-lang-client-0386264733.spotify_api_data.track_details` td
    ON st.track_id = td.track_id

-- Here I simply join two tables by their track id, in that way I have table with all data that I need.