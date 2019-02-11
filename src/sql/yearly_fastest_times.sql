SELECT
  CAST(substr(datetime(m.date, 'unixepoch'), 0, 5) AS INT) AS year
  , CASE WHEN r.time > 90 * 60 THEN time(r.time, 'unixepoch')
       WHEN (r.time % 60) < 10 THEN CAST(r.time / 60 AS int) || ':0' || (r.time % 60)
      ELSE CAST(r.time / 60 AS int) || ':' || (r.time % 60) END AS time
  , a.name AS athlete
  , m.name AS meeting
FROM results r
JOIN meetings m ON m.id = r.meeting_id
JOIN athletes a ON a.id = r.athlete_id
JOIN (
SELECT
  female
  , event_id
  , min(time) AS t
  , CAST(substr(datetime(m.date, 'unixepoch'), 0, 5) AS INT) AS year
FROM results r
JOIN events e ON e.id = r.event_id
JOIN meetings m ON m.id = r.meeting_id
JOIN athletes a ON a.id = r.athlete_id
WHERE event_id = @option
AND female IN (@gender)
GROUP BY year) fastest
ON fastest.year = CAST(substr(datetime(m.date, 'unixepoch'), 0, 5) AS INT)
AND fastest.female = a.female
AND fastest.t = r.time
AND fastest.event_id = r.event_id
ORDER BY year DESC