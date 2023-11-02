
CREATE DATABASE work;



CREATE TABLE job(
  id VARCHAR(255),
  job_title VARCHAR(50),
  job_location VARCHAR(50),
  job_description VARCHAR(9000),
  company_name VARCHAR(50),
  company_size INT,
  company_founde VARCHAR(50),
  company_type VARCHAR(50),
  company_industry VARCHAR(50),
  company_sector VARCHAR(50),
  company_revenue VARCHAR(50),
  stars INT,
  min_salary INT,
  max_salary INT
)








## list number of uer skills appeared in job description sorted in descending order 
WITH SkillMatches AS (
  SELECT j.id, j.job_titile, j.job_description, s.skill
  FROM job j
  LEFT JOIN (
    SELECT id, unnest(REGEXP_MATCHES(job_description, '(?i)[^\w](java|python|bi)(?![\w])', 'g')) AS skill
    FROM job
  ) s
  ON j.id = s.id
)
SELECT j.id, j.job_titile, j.job_description, COUNT(DISTINCT LOWER(s.skill)) AS unique_skill_count
FROM job j
LEFT JOIN SkillMatches s ON j.id = s.id
GROUP BY j.id, j.job_titile, j.job_description
HAVING COUNT(DISTINCT s.skill) > 0
ORDER BY unique_skill_count DESC;


