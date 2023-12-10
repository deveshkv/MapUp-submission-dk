import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
   # Pivot the DataFrame to create the desired matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
    #Due to above line data set having null values at diagonal
    # Fill missing values with 0
    car_matrix.fillna(0, inplace=True)
    
    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
     # Using value_counts to count occurrences of each car type
    df['car'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_counts = df['car'].value_counts().to_dict()
    type_counts = dict(sorted(type_counts.items()))
    return type_counts
   


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
     # Calculate the mean of 'bus' values
    bus_mean = df['bus'].mean()
    
    # Find indexes where 'bus' values exceed twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    
    return sorted(bus_indexes)

  


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Group by 'route' and calculate the mean of 'truck' values for each route
    route_means = df.groupby('route')['truck'].mean()
    
    # Filter routes with average 'truck' values greater than 7
    selected_routes = route_means[route_means > 7].index.tolist()
    
    return selected_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
     # Custom condition: Multiply values by 2 if greater than 20, otherwise multiply by 1.25
    modified_matrix = result1.copy()
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x*1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
   def verify_time_completeness(df):
   
    # Combine startDay and startTime to create the 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    
    # Combine endDay and endTime to create the 'end_timestamp' column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    
    # Extract day of the week and hour from start_timestamp
    df['day_of_week'] = df['start_timestamp'].dt.dayofweek
    df['hour'] = df['start_timestamp'].dt.hour

    # Group by (id, id_2) and check completeness
    completeness_check = df.groupby(['id', 'id_2']).apply(check_completeness)

    return completeness_check

def check_completeness(group):
    """
    Check completeness of time data for a specific (id, id_2) pair.

    Args:
        group (pandas.DataFrame): Grouped DataFrame for a specific (id, id_2) pair.

    Returns:
        bool: True if timestamps are complete, False otherwise.
    """
    # Check if timestamps cover a full 24-hour period
    hours_covered = set(group['hour'])
    full_day_coverage = len(hours_covered) == 24

    # Check if timestamps span all 7 days of the week
    days_covered = set(group['day_of_week'])
    full_week_coverage = len(days_covered) == 7

    # Return True if timestamps are complete, False otherwise
    return full_day_coverage and full_week_coverage
