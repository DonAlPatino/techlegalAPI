select date(created_at),count(*) from techlegal.techlegal_subjects group by date(created_at);
select date(created_at),count(*) from techlegal.techlegal_requests group by date(created_at);
select date(created_at),count(*) from techlegal.techlegal_credits group by date(created_at);
SELECT * FROM techlegal.techlegal_requests  ORDER BY id DESC LIMIT 1;