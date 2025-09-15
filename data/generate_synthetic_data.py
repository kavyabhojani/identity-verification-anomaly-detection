import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

fake = Faker()
random.seed(42)
np.random.seed(42)

def simulate_users(n_users: int = 20000):
    users = []
    for _ in range(n_users):
        users.append({
            "user_id": fake.uuid4(),
            "home_country": random.choice(["CA","US","UK","DE","FR","IN","AU"]),
            "signup_ts": fake.date_time_between(start_date="-2y", end_date="-6m", tzinfo=timezone.utc)
        })
    return pd.DataFrame(users)

def simulate_logins(users: pd.DataFrame, n_logins: int = 200000, anomaly_rate: float = 0.06):
    devices = [f"dev_{i:05d}" for i in range(10000)]
    geo_regions = ["CA","US","UK","DE","FR","IN","AU","BR","SG","JP","MX"]
    rows = []
    for _ in range(n_logins):
        u = users.sample(1).iloc[0]
        user_id = u["user_id"]
        login_time = fake.date_time_between(start_date="-180d", end_date="now", tzinfo=timezone.utc)
        device_id = random.choice(devices)
        country = random.choice([u["home_country"]] * 6 + random.choices(geo_regions, k=4))
        ip_octets = [str(random.randint(1, 254)) for _ in range(4)]
        ip = ".".join(ip_octets)

        label = 0
        if np.random.rand() < anomaly_rate:
            label = 1
            t = np.random.rand()
            if t < 0.34:
                device_id = f"new_{random.choice(devices)}"  # sudden new device
            elif t < 0.68:
                country = random.choice(["CN","RU","IR","KP","NG","AR"])  # improbable geo
            else:
                login_time = login_time + timedelta(minutes=random.randint(1, 10))  # rapid login

        rows.append({
            "user_id": user_id,
            "login_time": login_time.isoformat(),
            "device_id": device_id,
            "country": country,
            "ip_address": ip,
            "label": label
        })
    return pd.DataFrame(rows)

def main():
    base = Path(__file__).resolve().parents[1]
    out_dir = base / "data"
    out_dir.mkdir(parents=True, exist_ok=True)

    users = simulate_users()
    logins = simulate_logins(users)

    users.to_csv(out_dir / "users.csv", index=False)
    logins.to_csv(out_dir / "synthetic_logins.csv", index=False)
    print(f"Wrote {len(users)} users -> {out_dir/'users.csv'}")
    print(f"Wrote {len(logins)} logins -> {out_dir/'synthetic_logins.csv'}")

if __name__ == "__main__":
    main()
