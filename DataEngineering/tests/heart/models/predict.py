
"""Module for training and serializing a Sklearn regression model."""

from typing import Dict, Union

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# removed roc_auc_score

SklearnRegressionModel = Union[RandomForestRegressor, LogisticRegression]


def predict_model(
    model: SklearnRegressionModel, features: pd.DataFrame
) -> np.ndarray:
    """Uses a trained Sklearn regression model to make predictions on new data."""
    predicts = model.predict(features)
    return predicts


def evaluate_model(
    predicts: np.ndarray, target: pd.Series
) -> Dict[str, float]:
    """Evaluates the performance of a trained Sklearn regression model
    by comparing its predictions to the true target values."""
    return {
        "accuracy": accuracy_score(target, predicts),
    }
