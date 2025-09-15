import duckdb
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data"
IMAGES = BASE / "images"

def main():
    users = pd.read_csv(DATA / "users.csv", parse_dates=["signup_ts"])
    logins = pd.read_csv(DATA / "synthetic_logins.csv", parse_dates=["login_time"])

    con = duckdb.connect(database=':memory:')
    con.register("users_t", users)
    con.register("logins_t", logins)

    sql_path = BASE / "src" / "features" / "sql_features.sql"
    sql = sql_path.read_text(encoding="utf-8")

    features = con.execute(sql).df()

    out_path = DATA / "features.parquet"
    features.to_parquet(out_path, index=False)
    print(f"Wrote features -> {out_path}  rows={len(features)}  cols={features.shape[1]}")

if __name__ == "__main__":
    main()
