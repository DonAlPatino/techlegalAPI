# techlegalAPI

alembic stamp head - set alembic current version without real change
alembic revision --autogenerate -m "Add techlegal_epexist table"
alembic revision --autogenerate -m "Add fields to techlegal_credits table"
alembic upgrade head
alembic downgrade -1

source venv/bin/activate
deactivate

CREDIT size: 192.76 MB
REQUEST size: 1163.71 MB
SUBJECT size: 670.66 MB
EPEXIST size: 108.32 MB

pywin32==310 only windows