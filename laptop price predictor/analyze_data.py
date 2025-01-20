import math
import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def get_basic_stats(df):
    num_of_laptops = len(df["price"])

    mean = statistics.mean(df["price"])
    median = statistics.median(df["price"])
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    IQR = q3-q1

    min = df["price"].min()
    max = df["price"].max() 
    range = max-min

    stdev = statistics.stdev(df["price"])

    print("Number of laptops: ", num_of_laptops)
    print("Mean: ", mean)
    print("Median: ", median)
    print("Q1: ", q1)
    print("Q3: ", q3)
    print("IQR: ", IQR)
    print("Min: ", min)
    print("Max: ", max)
    print("Range: ", range)
    print("Standard Deviation: ", stdev)
    print("Outliers: ", get_outliers(df))

def get_outliers(df):
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    IQR = q3-q1
    lower_bound = q1 - 1.5*IQR
    upper_bound = q3 + 1.5*IQR
    outliers = df[(df["price"] < lower_bound) | (df["price"] > upper_bound)]
    return outliers

