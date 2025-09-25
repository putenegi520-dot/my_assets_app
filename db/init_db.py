# filepath: db/init_db.py
"""
DB 初期化スクリプト（SQLite + SQLAlchemy）
実行: python db/init_db.py
"""
from sqlalchemy import create_engine
from models import Base

def init_db(path="sqlite:///assets.db"):
    engine = create_engine(path, echo=False, future=True)
    Base.metadata.create_all(engine)
    print("DB initialized:", path)

if __name__ == "__main__":
    init_db()
