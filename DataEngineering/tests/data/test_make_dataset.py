import pandas as pd

from heart.data.make_dataset import read_data, split_train_test_data
from heart.entities import SplittingConfig


def test_load_dataset(dataset_path: str, target_col: str):
    data = read_data(dataset_path)
    assert len(data) == 100
    assert target_col in data.keys(), (
            "target_col not in dataset"
        )


def test_split_dataset(dataset: pd.DataFrame):
    train, test = split_train_test_data(dataset, test_size=SplittingConfig.test_size, random_state=SplittingConfig.random_state)
    assert train.shape[0] == 75
    assert test.shape[0] == 25
