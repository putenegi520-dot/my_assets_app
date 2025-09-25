# filepath: scripts/import_excel.py
"""
簡易インポータのスケルトン:
    python scripts/import_excel.py data/sample/2023_summary.xlsx
（実装は要補完）
"""
import sys
import pandas as pd

def import_summary(path):
    df = pd.read_excel(path, sheet_name='summary')
    # TODO: melt して DB に挿入
    print("Loaded rows:", len(df))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_excel.py <xlsx_path>")
    else:
        import_summary(sys.argv[1])
