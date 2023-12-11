import pandas as pd
import numpy as np
df = pd.read_csv('dataset-3.csv')
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    unique_ids = sorted( list(set(df["id_start"].tolist()+df["id_end"].tolist() ) ))
    df = df.sort_values("id_start")
    df = df.groupby("id_start").agg(id_end=('id_end', 'min'), distance=('distance', 'min') ).reset_index()

    grid = pd.DataFrame(index=unique_ids, columns=unique_ids)
    np.fill_diagonal(grid.values, 0)
    k = 0
    for i in df.index:
        grid[df["id_start"][i]][df["id_end"][i]] = df['distance'][i]
        grid[df["id_end"][i]][df["id_start"][i]] = df['distance'][i]

        for j in range(k-1, -1, -1):
            grid[unique_ids[k+1]][unique_ids[j]] = grid[unique_ids[k]][unique_ids[j]] + grid[unique_ids[k+1]][unique_ids[j+1]]
            grid[unique_ids[j]][unique_ids[k+1]] = grid[unique_ids[k+1]][unique_ids[j]]
        k+=1   

    return grid


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
   unique_ids = sorted( list(set(df["id_start"].tolist()+df["id_end"].tolist() ) ))
    df = df.sort_values("id_start")
    df = df.groupby("id_start").agg(id_end=('id_end', 'min'), distance=('distance', 'min') ).reset_index()

    grid = pd.DataFrame(index=unique_ids, columns=unique_ids)
    np.fill_diagonal(grid.values, 0)
    k = 0

    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    avg = np.average(df[ref])
    maxi = avg*1.1
    mini = avg*0.9
    li = []
    for i in df.index:
        if mini <= df[ref][i] <= maxi:
            li.append(df[ref][i])
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    if row['start_day'] in ['Saturday', 'Sunday']:
            return row['distance'] * discount_factor_weekends
        else:
            for time_range, discount_factor in zip(time_ranges_weekdays, discount_factors_weekdays):
                start_time, end_time = time_range
                if start_time <= row['start_time'] <= end_time and start_time <= row['end_time'] <= end_time:
                    return row['distance'] * discount_factor


    df['time_based_toll'] = df.apply(calculate_toll_rate, axis=1)

    return df
