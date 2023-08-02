"""
This module defines a dataclass, FeatureConfig, used for configuring features in a dataset.
It provides a structured way to specify categorical features, numerical features, target column(s),
and additional options for feature processing.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass()
class FeatureConfig:
    """A dataclass that represents the feature configuration for a dataset."""
    categorical_features: List[str]
    numerical_features: List[str]
    target_col: List[str]
    use_log_trick: bool = field(default=True)
    features_to_drop: Optional[List[str]] = None
