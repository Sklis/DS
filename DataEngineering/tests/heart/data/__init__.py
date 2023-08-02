"""
This module provides utility functions for handling datasets.
It includes two main functions, "read_data" and "split_train_test_data".
"""

from .make_dataset import read_data, split_train_test_data

__all__ = ["read_data", "split_train_test_data"]
