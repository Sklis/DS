"""
Module for learning model on data of heart illnesses.
It performs data loading, preprocessing, feature engineering, model training,
prediction, and evaluation. The pipeline supports configuration through a Hydra configuration
file.
"""

import os
import json
import logging
import logging.config

import hydra
import pandas as pd
# from hydra.utils import get_original_cwd

from entities import TrainingPipelineConfig  # pylint: disable=E0401
from data import read_data, split_train_test_data  # pylint: disable=E0401
from features import build_transformer, make_features, extract_target  # pylint: disable=E0401
from models import train_model, predict_model, evaluate_model  # pylint: disable=E0401
# removed serialize_model

logger = logging.getLogger(__name__)


def prepare_val_features_for_predict(
        train_features: pd.DataFrame, val_features: pd.DataFrame
):
    """ Function for preparing val_features for predict """
    train_features, val_features = train_features.align(
        val_features, join="left", axis=1
    )
    val_features = val_features.fillna(0)
    return val_features


def train_pipeline(params: TrainingPipelineConfig) -> None:
    """E2E train pipeline function"""
    logger.info("Starting pipeline")
    data = read_data(params.dataset.input_data_path)
    logger.info("data.shape is %s", {data.shape})

    # added 4 lines
    train_df, test_df = split_train_test_data(
        data, params.split.test_size,
        params.split.random_state
    )

    logger.info("Starting transforms")
    transformer = build_transformer(
        categorical_features=params.feature.categorical_features,
        numerical_features=params.feature.numerical_features,
    )
    transformer.fit(train_df)
    train_features = make_features(transformer, train_df)
    train_target = extract_target(train_df, params.feature.target_col)
    logger.info("train_features.shape is %s", {train_features.shape})

    model = train_model(
        params.model.model_params,
        train_features, train_target
    )

    test_features = make_features(transformer, test_df)
    test_target = extract_target(test_df, params.feature.target_col)

    val_features_prepared = prepare_val_features_for_predict(
        train_features, test_features
    )
    logger.info("test_features.shape is %s", {val_features_prepared.shape})
    predicts = predict_model(
        model,
        val_features_prepared
    )

    metrics = evaluate_model(
        predicts,
        test_target
    )

    metrics_output_dir = os.path.join(os.getcwd(), 'metrics')
    model_output_dir = os.path.join(os.getcwd(), 'models')

    os.makedirs(metrics_output_dir, exist_ok=True)
    metrics_filepath = os.path.join(metrics_output_dir, f"{params.model.model_name}.json")
    with open(metrics_filepath, "w", encoding="utf-8") as metric_file:
        json.dump(metrics, metric_file)
    logger.info(f"metrics is {metrics}")
    logger.info("metrics saved to %s", {metrics_filepath,})

    os.makedirs(model_output_dir, exist_ok=True)
    models_filepath = os.path.join(model_output_dir, f"{params.model.model_name}.pkl")
    # path_to_model = serialize_model(model, models_filepath)
    logger.info("model saved to %s", {models_filepath,})

    logger.info("Finish train")


@hydra.main(config_path="../configs", config_name="config", version_base=None)
def main(cfg: TrainingPipelineConfig) -> None:
    """Main function for setting logger and run train_pipeline"""
    train_pipeline(cfg)


if __name__ == "__main__":
    main()
