"""
Data Processing Module

This module contains functions and classes for processing
categorical and numerical features in a dataset.
It provides pipelines for transforming categorical features
using one-hot encoding and filling missing values,
as well as processing numerical features by removing
outliers and applying standard scaling.
"""

from typing import List

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler


def process_categorical_features(categorical_df: pd.DataFrame) -> pd.DataFrame:
    """Processes categorical features in a DataFrame using
    a categorical pipeline and returns the transformed DataFrame"""
    categorical_pipeline = build_categorical_pipeline()
    return pd.DataFrame(categorical_pipeline.fit_transform(categorical_df).toarray())


def build_categorical_pipeline() -> Pipeline:
    """Builds a pipeline for processing categorical features,
    including an imputer for missing values and one-hot encoding."""
    categorical_pipeline = Pipeline(
        [
            # added imputer
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder()),
        ]
    )
    return categorical_pipeline


def process_numerical_features(numerical_df: pd.DataFrame) -> pd.DataFrame:
    """Processes numerical features in a DataFrame using
    a numerical pipeline and returns the transformed DataFrame."""
    num_pipeline = build_numerical_pipeline()
    return pd.DataFrame(num_pipeline.fit_transform(numerical_df))


def build_numerical_pipeline() -> Pipeline:
    """Builds a pipeline for processing numerical features,
    including an outlier remover and standard scaler."""
    num_pipeline = Pipeline(
        [
            # added outlier_remover and scaler
            ("outlier_remover", OutlierRemover()),
            ("scaler", StandardScaler())
        ]
    )
    return num_pipeline


def make_features(transformer: ColumnTransformer, data_frame: pd.DataFrame) -> pd.DataFrame:
    """Transforms a DataFrame using a provided ColumnTransformer object
    and returns the transformed DataFrame."""
    return pd.DataFrame(transformer.transform(data_frame))


def extract_target(data_fr: pd.DataFrame, target_col: List[str]) -> pd.Series:
    """Extracts the target variable from a DataFrame given the target column(s)"""
    target = data_fr[target_col].values
    return target


class OutlierRemover(BaseEstimator, TransformerMixin):
    """
    A transformer class that removes outliers from numerical features.
    It implements the BaseEstimator and TransformerMixin interfaces from scikit-learn
    """
    def __init__(self, factor=1.5):
        self.factor = factor

    def outlier_removal(self, data_name: pd.DataFrame):
        """Removes outliers from a given DataFrame using the factor parameter."""
        data_name = pd.Series(data_name).copy()
        q_1 = data_name.quantile(0.25)
        q_3 = data_name.quantile(0.75)
        iqr = q_3 - q_1
        lower_bound = q_1 - (self.factor * iqr)
        upper_bound = q_3 + (self.factor * iqr)
        data_name.loc[((data_name < lower_bound) | (data_name > upper_bound))] = np.nan
        return pd.Series(data_name)

    def fit(self, feat, targ=None):
        """Returns the transformer object."""
        return self

    def transform(self, data: np.array):
        """Applies the outlier removal to a NumPy array."""
        return pd.DataFrame(data).apply(self.outlier_removal)


def build_transformer(
        categorical_features: List[str], numerical_features: List[str]
) -> ColumnTransformer:
    """
    Builds a ColumnTransformer object
    for processing both categorical and numerical features
    using the respective pipelines.
    """
    transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                build_categorical_pipeline(),
                # [c for c in categorical_features],
                list(categorical_features),
            ),
            # added numerical_pipeline
            (
                "numerical_pipeline",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("scaler", StandardScaler()),
                ]),
                list(numerical_features),
            )
        ]
    )
    return transformer
