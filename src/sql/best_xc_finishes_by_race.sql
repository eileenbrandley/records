SELECT
  a.name AS athlete
    , e.name AS race
    , m.name AS meeting
    , MIN(r.position) AS 'top finish'
    , MAX(r.position) AS 'worst finish'
    , ROUND(AVG(r.position), 2) AS 'average position'
    , CASE WHEN (AVG(r.time) % 60) < 10 THEN CAST(AVG(r.time) / 60 AS int) || ':0' || (AVG(r.time) % 60)
           ELSE CAST(AVG(r.time) / 60 AS int) || ':' || (AVG(r.time) % 60) END AS 'average finishing time'
    , COUNT(r.position) AS 'races'
FROM results r
       JOIN athletes a ON a.id = r.athlete_id
       JOIN events e ON e.id = r.event_id
       JOIN meetings m ON m.id = r.meeting_id
       JOIN championship_races ch ON ch.id = m.championship_race_id
WHERE ch.id = @option
  AND a.female IN (@gender)
GROUP BY a.id ORDER BY MIN(r.position)