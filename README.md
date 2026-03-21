============
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install --upgrade pip --index-url https://mirrors.sustech.edu.cn/pypi/web/simple
pip install -r requirements.txt -i https://mirror.yandex.ru/simple

pip install -r requirements.txt

pip install httpx[socks]

pip install cffi --only-binary :all:
pip install pydantic_core --only-binary :all:
=============


docker compose up
alembic upgrade head
Не забудь .env!!!


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

docker run -d \
    --name mtproxy \
    -p 1080:1080 \
    -e SOCKS5_HOST=127.0.0.1 \
    -e SOCKS5_PORT=1080 \
    -e SECRET=ваш_секрет_из_телеграм \
    ghcr.io/nick3/mt2socks5:release