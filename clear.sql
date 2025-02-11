DELETE FROM techlegal_credits
WHERE created_at < NOW() - INTERVAL 2 DAY
AND EXISTS (
    SELECT 1
    FROM (SELECT * FROM techlegal_credits) AS tmp
    WHERE DATE(tmp.created_at) = CURDATE()
);

DELETE FROM techlegal_subjects
WHERE created_at < NOW() - INTERVAL 2 DAY
AND EXISTS (
    SELECT 1
    FROM (SELECT * FROM techlegal_subjects) AS tmp
    WHERE DATE(tmp.created_at) = CURDATE()
);

DELETE FROM techlegal_requests
WHERE created_at < NOW() - INTERVAL 2 DAY
AND EXISTS (
    SELECT 1
    FROM (SELECT * FROM techlegal_requests ) AS tmp
    WHERE DATE(tmp.created_at) = CURDATE()
);