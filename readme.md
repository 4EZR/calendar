# Bikin Env jika belum
https://www.anaconda.com/download/success
conda create --name myenv python=3.8
conda activate myenv

Cara Run FAST Api
1. pip install -r requirements.txt (package.json nya fastapi)
contoh:

# FastAPI and ASGI server
fastapi==0.112.2
uvicorn[standard]==0.22.0
pydantic==2.8.2
pony==0.7.19

# JWT
PyJWT==2.9.0
passlib[bcrypt]==1.7.4

# Firebase Admin SDK
firebase-admin==6.1.0

# Database ORM and migrations
sqlalchemy==2.0.15
alembic==1.11.1
pymysql==1.0.3
# pymysql==1.0.3

# Environment variables
python-dotenv==1.0.0

# HTTP client for testing and external API calls
httpx==0.24.1

# Background tasks and job queuing (optional, include if needed)
# celery==5.3.0
redis== 5.0.8
----------------------------------------------------------------

2. uvicorn src.main:app --reload  (start project fast api)
# src.main berubah berubah tergantung folder main.py dimana


4. stagger  http://127.0.0.1:8000/docs (link stagger fastapi)
5. conda env list (list env yang ada)
