import math
import statistics
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("output.csv")
    df['price'] = df['price'].str.replace('[\$,]', '', regex=True).astype(float).astype(int)
    print("Mean price: $"+ str(statistics.mean(df["price"])))
    print("Median price: $"+ str(statistics.median(df["price"])))

