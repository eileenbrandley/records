SELECT
  CAST(substr(datetime(m.date, 'unixepoch'), 0, 5) AS INT) AS year
  , e.name AS event
    , CASE WHEN r.time > 90 * 60 THEN time(r.time, 'unixepoch')
          WHEN (r.time % 60) < 10 THEN CAST(r.time / 60 AS int) || ':0' || (r.time % 60)
          ELSE CAST(r.time / 60 AS int) || ':' || (r.time % 60) END AS time
  , COUNT(r.id) AS count
FROM results r
JOIN events e ON e.id = r.event_id
JOIN meetings m ON m.id = r.meeting_id
JOIN athletes a ON a.id = r.athlete_id
WHERE r.event_id = @option
  AND female IN (@gender)
  -- AND datetime(m.date - a.dob/1000, 'unixepoch') - datetime(0, 'unixepoch') BETWEEN @lower AND @upper
GROUP BY r.event_id, year
ORDER BY year DESC