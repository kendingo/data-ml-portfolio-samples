-- Find the most expensive queries in a BigQuery project over the last 7 days.
-- Portfolio sample. Adjust the region qualifier (region-eu / region-us) as needed.
SELECT
  user_email,
  job_id,
  creation_time,
  ROUND(total_bytes_billed / POW(1024, 4), 4)             AS tib_billed,
  ROUND(total_bytes_billed / POW(1024, 4) * 6.25, 2)      AS approx_usd_on_demand,
  ROUND(total_slot_ms / 1000 / 3600, 3)                   AS slot_hours,
  SUBSTR(query, 1, 200)                                    AS query_preview
FROM `region-eu`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
  AND error_result IS NULL
ORDER BY total_bytes_billed DESC
LIMIT 25;

-- Typical fixes: select only needed columns, filter on the partition column,
-- cluster on common filter keys, and materialise repeated heavy joins.
