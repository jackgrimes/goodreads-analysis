import os
from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt

from configs import data_path


def plot_time_series(s, title):
    plt.plot(s)
    plt.grid(True)
    plt.title(title)
    plt.text(s.index[-1], s[-1], str(s[-1]))
    plt.text(s.index[-0], s[-0], str(s[-0]))
    plt.show()


def harmonize_index(col, df, min_date, max_date):
    df_harmonized = df.copy()[[col, "count"]]
    df_harmonized = df_harmonized.groupby([col]).sum()

    idx = pd.date_range(min_date, max_date)
    df_harmonized = df_harmonized.reindex(idx, fill_value=0)

    df_harmonized.columns = [
        c.replace("count", col).replace("Date ", "") for c in df_harmonized.columns
    ]

    return df_harmonized


def get_daily_counts_cumulative(df_goodreads):
    min_date = min(df_goodreads["Date Read"].min(), df_goodreads["Date Added"].min())
    max_date = pd.to_datetime(datetime.today())

    df_added = harmonize_index("Date Added", df_goodreads, min_date, max_date)
    df_read = harmonize_index("Date Read", df_goodreads, min_date, max_date)

    daily_counts = pd.concat([df_added, df_read], axis=1)

    daily_counts_cumulative = daily_counts.cumsum()

    return daily_counts_cumulative


def separate_pre_goodreads_books(df):
    df = df.copy()
    df_read_pre_goodreads = df[(df["Date Read"].isnull() & (df["Read Count"] > 0))]
    df_goodreads = df[~(df["Date Read"].isnull() & (df["Read Count"] > 0))]
    return df_goodreads, df_read_pre_goodreads


def read_in_the_data():
    df = pd.read_csv(
        os.path.join(data_path, "goodreads_library_export.csv"),
        parse_dates=["Date Added", "Date Read"],
    )
    df["count"] = 1
    return df


def show_days_to_read(df):
    df["days_to_read"] = (df["Date Read"] - df["Date Added"]).dt.days
    df["days_to_read"].hist(bins=50)
    plt.title("Days to read")
    plt.show()
    df["days_to_read"][df["days_to_read"] < 200].hist(bins=50)
    plt.title("Days to read under 200 days")
    plt.show()

    print("\nSlowest book (time from adding to read):")
    slowest = df[df["days_to_read"] == df["days_to_read"].max()]
    for title, days in zip(slowest["Title"], slowest["days_to_read"]):
        print("{}, ({} days)".format(title, days))

    print("\nFastest book (time from adding to read):")
    fastest = df[df["days_to_read"] == df["days_to_read"].min()]
    for title, days in zip(fastest["Title"], fastest["days_to_read"]):
        print("{}, ({} days)".format(title, days))


def book_scores(df):
    df["Average Rating"].hist(bins=20)
    plt.show()

    print("\nMin average rating:")
    min = df[df["Average Rating"] == df["Average Rating"].min()]
    for title, rating in zip(min["Title"], min["Average Rating"]):
        print("{}, ({} average rating)".format(title, rating))

    print("\nMax average rating:")
    max = df[df["Average Rating"] == df["Average Rating"].max()]
    for title, rating in zip(max["Title"], max["Average Rating"]):
        print("{}, ({} average rating)".format(title, rating))
