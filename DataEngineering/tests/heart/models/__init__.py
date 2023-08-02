"""Returns:
- Trained Sklearn regression model (train_model).
- File path of the serialized model (serialize_model).
- Numpy array of predicted values (predict_model).
- Dictionary of evaluation metrics (evaluate_model).
"""

from .fit import (
    train_model,
    serialize_model,
)

from .predict import (
    predict_model,
    evaluate_model,
)

__all__ = [
    "train_model",
    "serialize_model",
    "evaluate_model",
    "predict_model",
]
