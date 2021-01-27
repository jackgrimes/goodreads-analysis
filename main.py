from utils import (
    separate_pre_goodreads_books,
    get_daily_counts_cumulative,
    plot_time_series,
    read_in_the_data,
    show_days_to_read,
    book_scores,
)

if __name__ == "__main__":

    df = read_in_the_data()

    (
        df_goodreads,
        df_read_pre_goodreads,
    ) = separate_pre_goodreads_books(df)
    daily_counts_cumulative = get_daily_counts_cumulative(df_goodreads)

    # Books read - -1 to account for book currently reading
    daily_read_counts = daily_counts_cumulative["Read"] + len(df_read_pre_goodreads) - 1
    plot_time_series(daily_read_counts, "Books read")

    # Books to read
    daily_counts_cumulative["to_read"] = (
        daily_counts_cumulative["Added"] - daily_counts_cumulative["Read"]
    )
    plot_time_series(daily_counts_cumulative["to_read"], "Books to read", ylim=True, grid=True)

    # Days from added to read
    show_days_to_read(df_goodreads)

    # Book scores
    book_scores(df)
