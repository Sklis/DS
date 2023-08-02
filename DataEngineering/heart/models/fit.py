"""Module for training and serializing a Sklearn regression model."""

import pickle
from typing import Union

import pandas as pd
from hydra.utils import instantiate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


SklearnRegressionModel = Union[RandomForestClassifier, LogisticRegression]


def train_model(
    model_params, train_features: pd.DataFrame, target: pd.Series
) -> SklearnRegressionModel:
    """Trains a Sklearn regression model
    using the provided model parameters, training features, and target."""
    model = instantiate(model_params).fit(train_features, target)
    return model


def serialize_model(model: SklearnRegressionModel, output: str) -> str:
    """Serializes the trained model and saves it to the specified output file."""
    with open(output, "wb") as file:
        pickle.dump(model, file)
    return output
