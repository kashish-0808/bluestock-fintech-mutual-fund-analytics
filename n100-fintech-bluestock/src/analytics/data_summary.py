import pandas as pd
import os

folder = "data/processed"

for file in os.listdir(folder):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(folder, file))

        print("\n" + "="*40)
        print(file)
        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])
        print("Column Names:")
        print(list(df.columns))