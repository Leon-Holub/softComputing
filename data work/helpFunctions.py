import pandas as pd


def read_data(path):
    df = pd.read_csv(path)
    return df


def get_games_from_to(df, yearFrom, yearTo):
    return df[(df['Year'] >= yearFrom) & (df['Year'] <= yearTo)]
