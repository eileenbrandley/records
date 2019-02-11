SELECT
  ath.name
    , m.name AS meeting
    , CAST(substr(datetime(date, 'unixepoch'), 0, 5) AS INT) AS year
    , CASE WHEN f.f_time > 90 * 60 THEN time(f.f_time, 'unixepoch')
          WHEN (f.f_time % 60) < 10 THEN CAST(f.f_time / 60 AS int) || ':0' || (f.f_time % 60)
           ELSE CAST(f.f_time / 60 AS int) || ':' || (f.f_time % 60) END AS time
FROM results r1
     JOIN (
     SELECT
     r.athlete_id
    , r.event_id
    , MIN(r.time) AS f_time
     FROM results r
     WHERE r.event_id = @option
     GROUP BY athlete_id) f
ON r1.athlete_id = f.athlete_id AND r1.time = f.f_time AND r1.event_id = f.event_id
   JOIN athletes ath ON ath.id = r1.athlete_id
   JOIN events e1 ON e1.id = f.event_id
   JOIN meetings m ON m.id = r1.meeting_id
   AND female IN (@gender)
   -- AND datetime(m.date - ath.dob / 1000, 'unixepoch') - datetime(0, 'unixepoch') BETWEEN @lower AND @upper
GROUP BY r1.athlete_id ORDER BY r1.time