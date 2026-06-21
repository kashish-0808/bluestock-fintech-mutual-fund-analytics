import requests
import pandas as pd

schemes = {
    "HDFC Top 100": 125497,
    "SBI Bluechip": 119551,
    "ICICI Bluechip": 120503,
    "Nippon Large Cap": 118632,
    "Axis Bluechip": 119092
}

all_data = []

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url).json()

    nav_list = response["data"]

    df = pd.DataFrame(nav_list)
    df["scheme_name"] = name
    df["amfi_code"] = code

    all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)

print(final_df.head())
print(final_df.shape)

final_df.to_csv("data/raw/live_nav_data.csv", index=False)
print("CSV saved successfully!")