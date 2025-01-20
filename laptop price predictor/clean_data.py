import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import ast

#remove lines that dont fit the columns
df = pd.read_csv('output.csv', on_bad_lines='skip')

#Drops NA values in df
# df = df.dropna(axis=0, how='any')

print(df["specs"][0])
print(type(df["specs"][0])) 

#Create new columns for cpu, ram, gpu, and storage
for i in range(len(df["price"])):
    cleaned_string = df["specs"][i].replace("None", "null").replace("'", "\"")  # Convert to valid JSON format
    dictionary = ast.literal_eval(cleaned_string.replace("null", "None"))

    df["CPU"] = dictionary.get("CPU")
    df["GPU"] = dictionary.get("GPU")
    df["RAM"] = dictionary.get("RAM")
    df["Storage"] = dictionary.get("Storage")







