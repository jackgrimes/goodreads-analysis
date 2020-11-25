import pandas as pd
import datetime
from datetime import timedelta, date
from matplotlib import pyplot as plt

df = pd.read_csv(
    r"C:\Users\Jack\Downloads\goodreads_library_export.csv",
    parse_dates=["Date Added", "Date Read"],
)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = df["Date Added"].min().date()
end_date = datetime.datetime.now().date() + timedelta(1)


def books_to_read(start_date, end_date):
    n_books_on_list = pd.DataFrame(columns=["date", "n"])
    for single_date in daterange(start_date, end_date):
        books_not_read = df[
            (
                (df["Date Added"] <= pd.to_datetime(single_date))
                & (
                    (df["Date Read"] >= pd.to_datetime(single_date))
                    | (df["Read Count"] == 0)
                ).astype(int)
            )
        ]
        print(single_date.strftime("%Y-%m-%d"), books_not_read.shape[0])
        n_books_on_list = pd.concat(
            [
                n_books_on_list,
                pd.DataFrame({"date": [single_date], "n": [books_not_read.shape[0]]}),
            ]
        )

    plt.plot(n_books_on_list["date"], n_books_on_list["n"])
    plt.grid(True)
    plt.title("Books to read")
    plt.show()


def books_read(start_date, end_date):
    read_books = pd.DataFrame(columns=["date", "n"])
    for single_date in daterange(start_date, end_date):
        books_read = df[
            (
                (df["Date Read"] <= pd.to_datetime(single_date))
                | ((df["Date Read"].isnull()) & (df["Read Count"] == 1)).astype(int)
            )
        ]
        print(single_date.strftime("%Y-%m-%d"), books_read.shape[0])
        read_books = pd.concat(
            [
                read_books,
                pd.DataFrame({"date": [single_date], "n": [books_read.shape[0]]}),
            ]
        )

    plt.plot(read_books["date"], read_books["n"])
    plt.grid(True)
    plt.title("Books read")
    plt.show()


books_to_read(start_date, end_date)

books_read(start_date, end_date)
