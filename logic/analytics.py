# filepath: logic/analytics.py
"""
analytics: DB 接続を受けて pandas DataFrame を返す最小実装のスケルトン
"""
import pandas as pd
from sqlalchemy import text

def get_latest_snapshot(conn) -> pd.DataFrame:
    # TODO: 実装 — 各資産の最新残高を返す
    df = pd.DataFrame([], columns=["asset_id", "name", "group", "date", "amount"])
    return df

def total_assets_by_date(conn, date=None) -> float:
    # TODO: 実装
    return 0.0
