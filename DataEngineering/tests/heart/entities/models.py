"""
Module defines dataclasses for configuring different machine learning models.
It provides a structured way to specify model parameters and their default values
for Random Forest and Logistic Regression models.
"""

from typing import Any
# removed Optional
from dataclasses import dataclass, field


@dataclass
class RFConfig:
    """A dataclass representing the configuration for a Random Forest model"""
    _target_: str = field(default='sklearn.ensemble.RandomForestClassifier')
    max_depth: int = field(default=3)
    n_estimators: int = field(default=100)
    random_state: int = field(default=42)

@dataclass
class LogregConfig:
    """A dataclass representing the configuration for a Logistic Regression model"""
    _target_: str = field(default='sklearn.linear_model.LogisticRegression')
    penalty: str = field(default='l1')
    solver: str = field(default='liblinear')
    C: float = field(default=1.0)
    random_state: int = field(default=42)
    max_iter: int = field(default=100)


@dataclass
class ModelConfig:
    """A dataclass representing the configuration for any model,
    consisting of a model name and its corresponding parameters."""
    model_name: str
    model_params: Any
