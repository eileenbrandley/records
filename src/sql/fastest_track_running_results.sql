SELECT
  e.name AS event
  , a.name AS athlete
  , CASE WHEN r.time > 90 * 60 THEN time(r.time, 'unixepoch')
        WHEN (r.time % 60) < 10 THEN CAST(r.time / 60 AS int) || ':0' || (r.time % 60)
        ELSE CAST(r.time / 60 AS int) || ':' || (r.time % 60) END AS time
  , CAST(substr(datetime(m.date, 'unixepoch'), 0, 5) AS INT) AS year
FROM results r
JOIN (
  SELECT
    r.id
    , MIN(r.time)
    , event_id
  FROM results r
  JOIN events e ON e.id = r.event_id
  JOIN athletes a ON a.id = r.athlete_id
  WHERE e.track = 1
  AND female IN (@gender)
  GROUP BY event_id) min_time
ON min_time.id = r.id
JOIN athletes a ON a.id = r.athlete_id
JOIN meetings m ON m.id = r.meeting_id
JOIN events e ON e.id = r.event_id
ORDER BY e.distance