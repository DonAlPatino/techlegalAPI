# techlegalAPI

alembic stamp head - set alembic current version without real change
alembic revision --autogenerate -m "Add techlegal_epexist table"
alembic upgrade head

source venv/bin/activate
deactivate