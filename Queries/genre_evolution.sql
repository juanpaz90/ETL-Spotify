CREATE OR REPLACE VIEW `gen-lang-client-0386264733.spotify_api_data.genre_evolution` AS
SELECT
    added_year,
    TRIM(genre) as genre,
    COUNT(*) as track_count
FROM `gen-lang-client-0386264733.spotify_api_data.enriched_tracks`,
UNNEST(SPLIT(artist_genres, ',')) as genre
WHERE artist_genres IS NOT NULL
GROUP BY added_year, genre
ORDER BY added_year, track_count DESC

-- Line 5
-- COUNT(*) means all rows in each group, in my case it counts how many rows I have in each group