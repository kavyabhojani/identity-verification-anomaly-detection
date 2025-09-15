-- sql_features.sql (DuckDB SQL)

-- Base tables are registered as 'users_t' and 'logins_t' by build_features.py

WITH device_counts AS (
  SELECT
    user_id,
    device_id,
    login_time,
    COUNT(DISTINCT device_id) OVER (
      PARTITION BY user_id
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS user_unique_devices_to_date
  FROM logins_t
),

time_diffs AS (
  SELECT
    user_id,
    device_id,
    country,
    login_time,
    ip_address,
    label,
    EXTRACT(EPOCH FROM (login_time - LAG(login_time) OVER (
      PARTITION BY user_id ORDER BY login_time
    ))) AS secs_since_prev_login
  FROM logins_t
),

geo_mismatch AS (
  SELECT
    t.user_id,
    t.login_time,
    t.country,
    u.home_country,
    CASE WHEN t.country <> u.home_country THEN 1 ELSE 0 END AS is_geo_mismatch
  FROM logins_t t
  JOIN users_t u USING(user_id)
),

velocity_24h AS (
  SELECT
    a.user_id,
    a.login_time,
    COUNT(*) AS logins_last_24h
  FROM logins_t a
  JOIN logins_t b
    ON a.user_id = b.user_id
   AND b.login_time BETWEEN a.login_time - INTERVAL '24 hours' AND a.login_time
  GROUP BY 1,2
)

SELECT
  l.user_id,
  l.login_time,
  l.device_id,
  l.country,
  l.ip_address,
  l.label,
  COALESCE(d.user_unique_devices_to_date, 1) AS user_unique_devices_to_date,
  COALESCE(td.secs_since_prev_login, 1e6) AS secs_since_prev_login,
  COALESCE(g.is_geo_mismatch, 0) AS is_geo_mismatch,
  COALESCE(v.logins_last_24h, 1) AS logins_last_24h
FROM logins_t l
LEFT JOIN device_counts d
  ON l.user_id = d.user_id AND l.login_time = d.login_time AND l.device_id = d.device_id
LEFT JOIN time_diffs td
  ON l.user_id = td.user_id AND l.login_time = td.login_time
LEFT JOIN geo_mismatch g
  ON l.user_id = g.user_id AND l.login_time = g.login_time
LEFT JOIN velocity_24h v
  ON l.user_id = v.user_id AND l.login_time = v.login_time
ORDER BY l.user_id, l.login_time;
