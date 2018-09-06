def pandas_index(column_name):
    import pandas as pd
    data = pd.read_csv('data-netflix.csv')
    return data[column_name]