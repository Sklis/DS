""" Module is providing a func for read data and slit it into train and test"""
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def read_data(dataset_path: str) -> pd.DataFrame:
    """Reading dataset from path"""
    data = pd.read_csv(dataset_path)
    return data


# added split_train_test_data function
def split_train_test_data(data: pd.DataFrame, test_size: float, random_state: int) -> pd.DataFrame:
    """Split dataset into random train and test subsets"""
    test_data, train_data = train_test_split(data, test_size=test_size, random_state=random_state)
    return test_data, train_data
