conda create --name myenv python=3.8
conda activate myenv

Cara Run FAST Api
1. pip install -r requirements.txt (package.json nya fastapi)
2. uvicorn src.main:app --reload  (start project fast api)
3. conda activate myenv (aktif environtment)
4. stagger  http://127.0.0.1:8000/docs (link stagger fastapi)
5. conda env list (list env yang ada)
