CREATE OR REPLACE VIEW `gen-lang-client-0386264733.spotify_api_data.genre_analysis` AS
SELECT
    TRIM(genre) as genre,
    COUNT(DISTINCT track_id) as track_count,
    AVG(popularity) as avg_popularity,
    AVG(duration_ms) as avg_duration_ms
FROM `gen-lang-client-0386264733.spotify_api_data.enriched_tracks`,
UNNEST(SPLIT(artist_genres, ',')) as genre
WHERE artist_genres IS NOT NULL
GROUP BY genre
HAVING track_count > 5
ORDER BY track_count DESC;

-- line 11 is to filter genres that appear less than 5 times,
-- I did that because it could be an `estrambotico` genre, so I do not take that in consideration