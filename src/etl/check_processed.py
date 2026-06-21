import os
import pandas as pd

PATH = "data/processed"

files = [f for f in os.listdir(PATH) if f.endswith(".csv")]

for f in files:
    df = pd.read_csv(os.path.join(PATH, f))
    print("\n", f)
    print("shape:", df.shape)
    print(df.head(1))