import math
import statistics
import pandas as pd
import numpy as np

# df = pd.read_csv("output.csv")
# # df = df[df['Specs'] != "{'manufacturer': 'Unable to find manufacturer', 'CPU': 'Unable to find CPU', 'RAM': 'Unable to find RAM', 'Storage': 'Unable to find Storage'}"]
# # df['price'] = df['price'].str.replace('[\$,]', '', regex=True).astype(float).astype(int)
# df_prices = df['price'].sort_values()
# df_prices = df_prices.tolist()
# print(df_prices)

def get_basic_stats(df):

    print("Mean price: $"+ str(statistics.mean(df["price"])))
    print("Median price: $"+ str(statistics.median(df["price"])))

    print("Standard Deviation: $"+ str(statistics.stdev(df["price"])))

