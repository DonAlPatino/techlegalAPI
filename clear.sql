DELETE FROM techlegal_credits
WHERE created_at < NOW() - INTERVAL 2 DAY
AND (SELECT COUNT(*) FROM techlegal_credits WHERE DATE(created_at) = CURDATE()) > 0;


DELETE FROM techlegal_requests
WHERE created_at < NOW() - INTERVAL 2 DAY
AND (SELECT COUNT(*) FROM techlegal_requests WHERE DATE(created_at) = CURDATE()) > 0;

DELETE FROM techlegal_subjects
WHERE created_at < NOW() - INTERVAL 2 DAY
AND (SELECT COUNT(*) FROM techlegal_subjects WHERE DATE(created_at) = CURDATE()) > 0;